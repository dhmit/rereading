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
            const res = await fetch('http://127.0.0.1:8000/api/');
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
                        <h1>{item.story}</h1>
                        <h3>{item.contexts[0]}</h3>
                        <p>{item.questions[0]['text']}</p>
                        <p>{item.questions[1]['text']}</p>
                        <h3>{item.contexts[1]}</h3>
                        <p>{item.questions[0]['text']}</p>
                        <p>{item.questions[1]['text']}</p>

                    </div>
                ))}
            </div>
        );
    }
}

export default InstructorPage