import React from 'react'
import './index.css';
import Table from 'react-bootstrap/Table'
import Form from "react-bootstrap/Form";
import Navbar from "react-bootstrap/Navbar";
import Button from "react-bootstrap/Button";

function Student(props) {
    const responses = props.student_responses.map(response => (
        <Response response={response} key={response.id}/>
    ));

    return (
        <div className='student'>
            <div><center><h1>Student #{props.id}</h1></center></div>
            <div><h5><b>Story: </b> {props.story}</h5></div>
            <Table striped bordered hover responsive>
                <thead>
                    <tr>
                        <td><b>Context</b></td>
                        <td><b>Question</b></td>
                        <td><b>Response</b></td>
                        <td><b>Views</b></td>
                    </tr>
                </thead>
                <tbody>{responses}</tbody>
            </Table>
        </div>
    );
}


function Response(props) {
    const response = props.response;

    return (
        <tr>
            <td>{response.context}</td>
            <td>{response.question}</td>
            <td>{response.response}</td>
            <td>{response.views}</td>
        </tr>
    );
}


class InstructorPage extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            students: [],
            loaded: false,
            filterBy: 'Student',
        };
    }

    async componentDidMount() {
        try {
            const res = await fetch('/api/add-response/');
            const students = await res.json();
            const filterBy = this.state.filterBy;
            this.setState({
                students,
                loaded: true,
                filterBy,
            });
        } catch (e) {
            console.log(e);
        }
    }

    handleSubmit(event) {
        const students = this.state.students;
        const loaded = this.state.loaded;
        this.setState({
            students,
            loaded,
            filter: event.target.value
        });
    }

    render() {
        if (this.state.loaded) {
            const students = this.state.students.map(student => (
                <Student story={student.story} student_responses={student.student_responses} id={student.id} key={student.id}/>
            ));

            return (
                <div>
                    <Navbar fixed={'top'}>
                        <form onSubmit={this.handleSubmit}>
                            <label>
                                Filter by
                                <select value={this.state.filter}>
                                    <option value={'Student'}>Student</option>
                                    <option value={'Story'}>Story</option>
                                    <option value={'Question'}>Question</option>
                                </select>
                            </label>
                            <input type={'submit'} value={'submit'}/>
                        </form>
                    </Navbar>
                    <div> {students} </div>
                </div>
            );
        } else {
            return null;
        }
    }
}

export default InstructorPage;
