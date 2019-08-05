import React from 'react';
import './index.css';
import Table from 'react-bootstrap/Table';
import Navbar from "react-bootstrap/Navbar";

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
                        <td><b>Scrolls</b></td>
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
            <td>{response.scroll_ups}</td>
        </tr>
    );
}

function QuestionView(props) {
    const students = props.students;
    let questions = {};
    for (let i = 0; i < students.length; i++) {
        let student = students[i];
        for (let prompt in student.student_responses) {
            let question = student.student_responses[prompt].question;
            let context = student.student_responses[prompt].context;
            if (questions.hasOwnProperty(context)) {
                if (questions[context].hasOwnProperty(question)) {
                    questions[context][question].push([i, prompt]);
                } else {
                    questions[context][question] = [[i, prompt]];
                }
            } else {
                questions[context] = {};
                questions[context][question] = [[i, prompt]];
            }
        }
    }

    const questionsToView = [];
    for (let context in questions) {
        for (let question in questions[context]) {
            questionsToView.push(
                <Question context={context} question={question} indices={questions[context][question]} students={students} key={context}/>
            );
        }
    }

    return (
        <div className='question-view'>
            {questionsToView}
        </div>
    );
}

function Question(props) {
    const responses = props.indices.map(index => (
        <QuestionResponse student={props.students[index[0]]} prompt={index[1]} key={index[0]}/>
    ));

    return (
        <div>
            <div><h2>Context: {props.context}</h2></div>
            <div><h2>Question: {props.question}</h2></div>
            <Table striped bordered hover responsive>
                <thead>
                <tr>
                    <td><b>Student</b></td>
                    <td><b>Response</b></td>
                    <td><b>Views</b></td>
                    <td><b>Scrolls</b></td>
                </tr>
                </thead>
                <tbody>{responses}</tbody>
            </Table>
        </div>
    );
}

function QuestionResponse(props) {
    return (
        <tr>
            <td>{props.student.id}</td>
            <td>{props.student.student_responses[props.prompt].response}</td>
            <td>{props.student.student_responses[props.prompt].views}</td>
            <td>{props.student.student_responses[props.prompt].scroll_ups}</td>
        </tr>
    );
}


class InstructorPage extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            students: [],
            loaded: false,
            sortBy: 'student',
        };

        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    async componentDidMount() {
        try {
            const res = await fetch('/api/add-response/');
            const students = await res.json();
            const sortBy = this.state.sortBy;
            this.setState({
                students,
                loaded: true,
                sortBy,
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
            sortBy: event.target.value
        });
    }

    handleChange(event) {
        const students = this.state.students;
        const loaded = this.state.loaded;
        this.setState({
            students,
            loaded,
            sortBy: event.target.value
        });
    }

    render() {
        if (this.state.loaded) {
            let tempStudents = [...this.state.students];
            let students;
            if (this.state.sortBy === 'story') {
                tempStudents.sort((a, b) => (a.story.toLowerCase() > b.story.toLowerCase() ? 1 : -1));
                students = tempStudents.map(student => (
                    <Student story={student.story} student_responses={student.student_responses} id={student.id} key={student.id}/>
                ));
            } else if (this.state.sortBy === 'question') {
                students = <QuestionView students={tempStudents}/>;
            } else {
                students = tempStudents.map(student => (
                    <Student story={student.story} student_responses={student.student_responses} id={student.id} key={student.id}/>
                ));
            }

            return (
                <div>
                    <Navbar fixed={'top'}>
                        <form onSubmit={this.handleSubmit}>
                            <label>
                                Sort by
                                <select value={this.state.sortBy} onChange={this.handleChange}>
                                    <option value={'student'}>Student</option>
                                    <option value={'story'}>Story</option>
                                    <option value={'question'}>Question</option>
                                </select>
                            </label>
                        </form>
                    </Navbar>
                    <div>
                        {students}
                    </div>
                </div>
            );
        } else {
            return null;
        }
    }
}

export default InstructorPage;
