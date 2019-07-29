import React from 'react'
import './index.css';
import Table from 'react-bootstrap/Table'

function Student(props) {
    console.log(props);
    const responses = props.student_responses.map(response => (
        <Response response={response} key={response.id}/>
    ));

    return (
        <div className='student'>
            Student #{props.id}
            <Table striped bordered hover responsive>
                <thead>
                    <tr>
                        <td>Context</td>
                        <td>Question</td>
                        <td>Response</td>
                        <td>Views</td>
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
        };
    }

    async componentDidMount() {
        try {
            const res = await fetch('/api/add-response/');
            const students = await res.json();
            this.setState({
                students,
                loaded: true,
            });
        } catch (e) {
            console.log(e);
        }
    }

    render() {
        // let index = 0;
        // let result;
        // if (index < (this.state.data.student_responses).length - 1) {
        //     result = (
        //         <div key={this.state.data.student_responses.id}>
        //             <h3>Context: {this.state.data.student_responses[index]['context']}</h3>
        //             <p>Question: {this.state.data.student_responses[index]['wuestion']}</p>
        //             <p>Response: {this.state.data.student_responses[index]['response']}</p>
        //             <p>Views: {this.state.data.student_responses[index]['views']}</p>
        //         </div>
        //     )
        //     index += 1;
        // }
        if (this.state.loaded) {
            const students = this.state.students.map(student => (
                <Student story={student.story} student_responses={student.student_responses} id={student.id} key={student.id}/>
            ));

            return students;
        } else {
            return null;
        }

        // return (
        //     <div>
        //         {this.state.students.map(item => (
        //             <div key={item.id} className={'box'}>
        //                 <h1>Story: {item.story}</h1>
        //                 <h3>Context: {item.student_responses[0]['context']}</h3>
        //                 <p>Questions: {item.student_responses[0]['question']}</p>
        //                 <p>Response: {item.student_responses[0]['response']}</p>
        //                 <p>Views: {item.student_responses[0]['views']}</p>
        //             </div>
        //         ))}
        //
        //     </div>
        // )
    }
}

export default InstructorPage;
