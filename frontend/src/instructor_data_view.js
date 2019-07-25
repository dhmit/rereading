import React from 'react'

class InstructorPage extends React.Component {
    constructor() {
        super();
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
        return (
            <div>
                {this.state.data.map(item => (
                    <div key={item.id}>
                        <h1>Story: {item.story}</h1>
                        <h3>Context: {item.student_responses[0]['context']}</h3>
                        <p>Question: {item.student_responses[0]['question']}</p>
                        <p>Response: {item.student_responses[0]['response']}</p>
                        <p>Views: {item.student_responses[0]['views']}</p>

                    </div>
                ))}
            </div>
        );
    }
}

export default InstructorPage