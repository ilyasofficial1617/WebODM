import React, { Component, Fragment } from "react";
import PropTypes from 'prop-types';

import ResizeModes from 'webodm/classes/ResizeModes';
import { Modal, Button } from "react-bootstrap";
import "./ImportView.scss";
import RCloneDialog from "./components/RCloneDialog"
import ConfigureNewTaskDialog from "./components/ConfigureNewTaskDialog"

export default class TaskView extends Component {
	static propTypes = {
		projectId: PropTypes.number.isRequired,
		apiURL: PropTypes.string.isRequired,
		onNewTaskAdded: PropTypes.func.isRequired,
	}

	state = {
		error : '',
		storageName : null,
		storagePath : null,
		isRCloneDialogOpen : false,
		isNewTaskDialogOpen : false,
	}

	onSaveTask = taskInfo => {
		
	}

	onErrorInDialog = msg => {
		this.setState({ error: msg });
		this.onCloseRCloneDialog();
	};

	handleImportButton = () => {
		this.setState({isRCloneDialogOpen : true});
		console.log("rclone dialog opened.");
	}

	onSubmitRCloneDialog = (storageName, storagePath) => {
		this.setState({
			storageName : storageName,
			storagePath : storagePath,
			isNewTaskDialogOpen : true,
		})
		console.log("rclone dialog submitted.")
		this.onCloseRCloneDialog()
	}

	onCloseRCloneDialog = () => {
		this.setState({isRCloneDialogOpen : false})
	}

	onHideConfigureNewTaskDialog = () => {
		this.setState({ 
			storageName : null,
			storagePath : null,
			isRCloneDialogOpen : false,
			isNewTaskDialogOpen : false,
		})
	}

	onSubmitConfigureNewTaskDialog = (taskInfo) => {
		console.log("onSubmitConfigureNewTaskDialog")
		// Create task
		const formData = {
				name: taskInfo.name,
				options: taskInfo.options,
				processing_node:  taskInfo.selectedNode.id,
				auto_processing_node: taskInfo.selectedNode.key == "auto",
				partial: true
		};

		console.log(formData.name)
		

		if (taskInfo.resizeMode === ResizeModes.YES){
				formData.resize_to = taskInfo.resizeSize;
		}

		console.log("try ajax")
		$.ajax({
				url: `/api/projects/${this.props.projectId}/tasks/`,
				contentType: 'application/json',
				data: JSON.stringify(formData),
				dataType: 'json',
				type: 'POST'
			}).done((task) => {
				console.log("done ajax")
				console.log('storage name')
				console.log(this.state.storageName)
				console.log('storage path')
				console.log(this.state.storagePath)
				$.ajax({
						url: `${this.props.apiURL}/projects/${this.props.projectId}/tasks/${task.id}/import`,
						contentType: 'application/json',
						data: JSON.stringify({storage_name: this.state.storageName, storage_path: this.state.storagePath}),
						dataType: 'json',
						type: 'POST'
					}).done(() => {
						this.onHideConfigureNewTaskDialog();
						this.props.onNewTaskAdded();
					}).fail(error => {
						this.onErrorInDialog("Failed to start importing.");
					});
			}).fail(() => {
				this.onErrorInDialog("Cannot create new task. Please try again later.");
			});
		
	}


	render() {
		return (
			<Fragment>
				{this.error ? <ErrorDialog errorMessage={this.error} /> : ""}
				<Button
					bsStyle={"default"}
					bsSize={"small"}
					onClick={this.handleImportButton}>
						<i className={"fas fa-archive"} />
						RClone Import
				</Button>
				{ 
					//conditional rendering
					this.state.isRCloneDialogOpen && 
					<RCloneDialog
						onSubmit={this.onSubmitRCloneDialog}
						onClose={this.onCloseRCloneDialog}
					/>
				}
				{
					this.state.isNewTaskDialogOpen &&
					<ConfigureNewTaskDialog
						apiURL={this.props.apiURL}
						onHide={this.onHideConfigureNewTaskDialog}
						onSaveTask={this.onSubmitConfigureNewTaskDialog}
					/>
				}
				
				{/*<RCloneDialog
					show={isRCloneDialogOpen}
					onHide={this.onHideRCloneDialog}
					onSubmit={this.onSubmitRCloneDialog}
				/>*/}
				{/*<ConfigureNewTaskDialog
					show={isNewTaskDialogOpen}
					apiURL={this.props.apiURL}
					onHide={this.onHideNewTaskDialog}
					onSubmit={this.onSubmitNewTaskDialog}
				/>
				*/}

			</Fragment>		
		);
	}
}
