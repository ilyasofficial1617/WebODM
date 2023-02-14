import PropTypes from 'prop-types';
import React, { Component, Fragment } from "react";
import { Modal, Button, FormGroup, Form, ControlLabel, FormControl, HelpBlock } from "react-bootstrap";
import Select from 'react-select';

export default class RCloneDialog extends Component {
	static defaultProps = {
		formName : "",
		formPath : "",
		onSubmit : null,
		onClose : null,
	};

	static propTypes = {
		onSubmit: PropTypes.func.isRequired,
		onClose: PropTypes.func.isRequired,
  	}

	resetState = () => {
		this.setState({formName:"",formPath:""});
	}

	handleSubmit = e => {
		this.props.onSubmit(this.state.formName, this.state.formPath)
		this.resetState()
	};

	handleClose = e => {
		this.props.onClose()
		this.resetState()
	}

	render() {
		const {
			onHide,
		} = this.props;

		return (
		    <div>
			  <Modal.Dialog>
			    <Modal.Header>
			      <Modal.Title>Import RClone</Modal.Title>
			    </Modal.Header>

			    <Modal.Body>
			    	<form id="form1">
			    		<FormGroup controlId="formName">
		          			<ControlLabel>Storage Name</ControlLabel>
		          			<FormControl 
		          				type="text"
		          				placeholder="name"
		          				onChange={e => this.setState({formName:e.target.value})}
		          			/>
		          		</FormGroup>
		          		<FormGroup controlId="formPath">
		          			<ControlLabel>Storage Path</ControlLabel>
		          			<FormControl 
		          				type="text"
		          				placeholder="path/to/folder"
		          				onChange={e => this.setState({formPath:e.target.value})}
		          			/>
		          		</FormGroup>
			    	</form>

			    </Modal.Body>

			    <Modal.Footer>
			    	<form id="form1">
				      <Button onClick={this.handleClose}>Close</Button>
				      <Button bsStyle="primary" onClick={this.handleSubmit}>Save changes</Button>
			      	</form>
			    </Modal.Footer>
			  </Modal.Dialog>
			</div>
		);
	}
}
