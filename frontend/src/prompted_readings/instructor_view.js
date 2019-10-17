import React from 'react';
import './instructor_view.css';
import PropTypes from "prop-types";

/**
 * A component that returns a simple table with all of the responses for a particular student
 *
 * Passes props.student_responses to Response component
 */
function Student(props) {
    const responses = props.student_responses.map(response => (
        <StudentResponse response={response} key={response.id}/>
    ));

    return (
        <div className='student'>
            <div className='student-number'><h1>Student #{props.id}</h1></div>
            <div><h5><b>Story: </b> {props.story}</h5></div>
            <table className="table striped bordered hover responsive">
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
            </table>
        </div>
    );
}
Student.propTypes = {
    id: PropTypes.number,
    student_responses: PropTypes.array,
    story: PropTypes.string,
};


/**
 * Returns a single table row given the response data
 *
 * For use with the Student component
 */
function StudentResponse(props) {
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
StudentResponse.propTypes = {
    response: PropTypes.object,
};


/**
 * Returns a page that sorts students' responses by the question that they are answering
 *
 * Passes data to Question component
 */
function QuestionView(props) {
    const students = props.students;
    let questions = {};

    // Sorts each student response by the context and question that they are answering
    // TODO: clean this up!
    for (let i = 0; i < students.length; i++) {

        const student = students[i];
        const student_responses = student.student_responses;

        // Iterate through all of the responses the student provided
        for (let response_num = 0; response_num < student_responses.length; response_num++) {

            const response = student_responses[response_num];
            const question = response.question;
            const context = response.context;

            // We have already added the context to our questions object
            if (questions.hasOwnProperty(context)) {

                const context_pairing = questions[context];

                // The question is already in the context's list, so add the student
                if (context_pairing.hasOwnProperty(question)) {
                    context_pairing[question].push([i, response_num]);

                // The context/question pairing doesn't exist yet
                } else {
                    context_pairing[question] = [[i, response_num]];
                }

            // The context doesn't exist yet, so add it to the questions object
            } else {
                questions[context] = {};
                questions[context][question] = [[i, response_num]];
            }
        }
    }

    // Create sections on the page dedicated to each Context/Question pairing
    const questionsToView = [];
    console.log(questions);

    // context_num is not guaranteed to start with 0
    for (let context_num in questions) {

        if (!questions.hasOwnProperty(context_num)) {
            continue;
        }

        const context_pairing = questions[context_num];

        for (let question in context_pairing) {

            if (!context_pairing.hasOwnProperty(question)) {
                continue;
            }

            questionsToView.push(
                <Question
                    context={context_num}
                    question={question}
                    indices={context_pairing[question]}
                    students={students}
                    key={context_num}
                />
            );
        }
    }

    return (
        <div className='question-view'>
            {questionsToView}
        </div>
    );
}
QuestionView.propTypes = {
    students: PropTypes.array,
};

/**
 * Creates a <div> that displays student response data for a particular question
 *
 * Requires 'indices' property to display
 */
function Question(props) {
    const responses = props.indices.map(index => (
        <QuestionResponse student={props.students[index[0]]} prompt_num={index[1]} key={index[0]}/>
    ));

    return (
        <div>
            <div><h2>Context: {props.context}</h2></div>
            <div><h2>Question: {props.question}</h2></div>
            <table className="table striped bordered hover responsive">
                <thead>
                    <tr>
                        <td><b>Student</b></td>
                        <td><b>Response</b></td>
                        <td><b>Views</b></td>
                        <td><b>Scrolls</b></td>
                    </tr>
                </thead>
                <tbody>{responses}</tbody>
            </table>
        </div>
    );
}
Question.propTypes = {
    indices: PropTypes.array.isRequired,
    students: PropTypes.array,
    context: PropTypes.string,
    question: PropTypes.string,
};


/**
 * Generates and returns a single row for the Question component
 */
class QuestionResponse extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            student: props.student,
            student_response: props.student.student_responses[props.prompt_num],
        }
    }

    render() {
        return (
            <tr>
                <td>{this.state.student.id}</td>
                <td>{this.state.student_response.response}</td>
                <td>{this.state.student_response.views}</td>
                <td>{this.state.student_response.scroll_ups}</td>
            </tr>
        );
    }
}
QuestionResponse.propTypes = {
    student: PropTypes.object,
    prompt_num: PropTypes.number,
};

/**
 * Main component for the Instructor view.
 * Accesses and maintains database data for student responses and handles
 * displaying the information properly on the page.
 */
class InstructorView extends React.Component {
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

    /**
     * This loads all of the data the moment the Instructor view is opened in the browser.
     *
     * If it cannot access the database, it logs the error
     */
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

    /**
     * Called when the user wishes to change the way that the data on the page is displayed
     * (i.e. by student, story, or question) and updates the state accordingly.
     */
    handleSubmit(event) {
        const students = this.state.students;
        const loaded = this.state.loaded;
        this.setState({
            students,
            loaded,
            sortBy: event.target.value
        });
    }

    /**
     * Whenever the user changes the value of the 'Sort by' dropdown menu,
     * this function is called and updates the state accordingly
     */
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
        if (this.state.loaded) {  // Only do this if we have the data! Otherwise breaks :(
            let tempStudents = this.state.students;
            console.log(tempStudents);
            let students;

            if (this.state.sortBy === 'story') { // If we're sorting by story
                const sorter = (a, b) => (a.story.toLowerCase() > b.story.toLowerCase() ? 1 : -1);
                tempStudents.sort((a, b) => sorter(a, b));
                students = tempStudents.map(student => (
                    <Student
                        story={student.story}
                        student_responses={student.student_responses}
                        id={student.id}
                        key={student.id}
                    />
                ));
            } else if (this.state.sortBy === 'question') {  // If we're sorting by the question
                students = <QuestionView students={tempStudents}/>;
            } else {  // By default, the Student view is displayed on page load
                students = tempStudents.map(student => (
                    <Student
                        story={student.story}
                        student_responses={student.student_responses}
                        id={student.id}
                        key={student.id}
                    />
                ));
            }

            return (
                <div>
                    <nav className="navbar fixed-top">
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
                    </nav>
                    <div>
                        {students}
                    </div>
                </div>
            );
        } else {
            // This ensures that our page doesn't get funky if we don't have data loaded properly
            return null;
        }
    }
}

export default InstructorView;
