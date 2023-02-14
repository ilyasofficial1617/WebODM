import PropTypes from 'prop-types';
import { Component } from "react";
import NewTaskPanel from "webodm/components/NewTaskPanel";
import { Modal, Button, FormGroup, Form, ControlLabel, FormControl, HelpBlock } from "react-bootstrap";

import "./ConfigureNewTaskDialog.scss";

export default class ConfigureNewTaskDialog extends Component {
	static defaultProps = {
		
	};

	static propTypes = {
		onHide: PropTypes.func.isRequired,
		onSaveTask: PropTypes.func.isRequired,
  	}

  	resetState = () => {
		
	}
	
  	render() {
		const {
			onHide,
			onSaveTask,
		} = this.props;

		return (
			<div>
			  <Modal.Dialog>
			    <Modal.Header>
			      <Modal.Title>Import RClone</Modal.Title>
			    </Modal.Header>

			    <Modal.Body>
			    	<NewTaskPanel
						onSave={onSaveTask}
						onCancel={onHide}
						filesCount={10}
						getFiles={() => []}
						showResize={false}
						suggestedTaskName={null}
					 />
			    </Modal.Body>
			  </Modal.Dialog>
			</div>
		);
	}
}
