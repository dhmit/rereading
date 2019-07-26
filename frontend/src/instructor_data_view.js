import React from 'react'
import './index.css';

function Responses(props) {

}

class InstructorPage extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            data: [],
        };
    }

    async componentDidMount() {
        try {
            const res = await fetch('http://127.0.0.1:8000/api/add-response');
            const data = await res.json();
            this.setState({
                data
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

        return (
            <div>
                {this.state.data.map(item => (
                    <div key={item.id} className={'box'}>
                        <h1>Story: {item.story}</h1>
                        <h3>Context: {item.student_responses[0]['context']}</h3>
                        <p>Questions: {item.student_responses[0]['question']}</p>
                        <p>Response: {item.student_responses[0]['response']}</p>
                        <p>Views: {item.student_responses[0]['views']}</p>
                    </div>
                ))};
                {/*result*/}
            </div>
        )
    }
}

export default InstructorPage;