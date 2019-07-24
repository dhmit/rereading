import React from 'react';
import './App.css';

// const list = [
//     {
//         id: 0,
//         story: 'Baby shoes. Never worn.',
//         contexts: ['This is an ad.', 'This is a story.'],
//         questions: [
//             {
//                 text: 'In one word or less, how did this make you feel?',
//                 word_limit: 1,
//             },
//             {
//                 text: 'In three words or less, what is this story about?',
//                 word_limit: 3,
//             },
//         ],
//     },
// ];

function Question(props) {
    return (
        <div className={'story'}>
            <div className={'context-text'}>{props.context}</div>
            <div className={'story-text'}>{props.story}</div>
            <div className={'question-prompt'}>{props.question}</div>
            <form onSubmit={props.onSubmit}>
                <label>
                    <input type={'text'} value={props.answer} onChange={props.onChange} />
                </label>
                <button type='submit'>Continue</button>
            </form>
        </div>
    );
}

class Study extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            story: null,
            contexts: [],
            questions: [],
            context_number: 0,
            question_number: 0,
            answers: [[]],
            finished: false,
            start: true,
            textInput: '',
        };

    }

    async componentDidMount() {
        // Load from server

        try {
            const questions = await fetch('http://localhost:8000/api/');
            const json = await questions.json();
            this.setState(json[0]);
        } catch (e) {
            console.log(e);
        }

        // this.setState(list[0])
    }

    postData() {
        const url = 'http://localhost:8000/api/';
        const data = {
            answers: this.state.answers,
        };
        console.log(JSON.stringify(data));

        fetch(url, {
            method: 'POST',
            body: JSON.stringify(data),
            headers: {
                'Content-type': 'application/json'
            }

        }).then(res => res.json()).then(response => console.log(JSON.stringify(response)))
            .catch(err => console.log(err));
    }

    handleFormChange(e) {
        this.setState({textInput: e.target.value});
    }

    validateSubmission(response, word_limit) {
        if (!response) {
            alert('Please enter a response.');
            return false;
        } else {
            const response_list = response.trim().split(' ');
            if (!(response_list.length <= word_limit)) {
                alert('Make sure to respect word limits.')
                return false;
            } 
        }

        return true;
    }


    handleSubmit(e) {
        e.preventDefault();
        let question_number = this.state.question_number;
        let context_number = this.state.context_number;
        const answers = this.state.answers.slice();
        const response = this.state.textInput;
        const word_limit = this.state.questions[question_number].word_limit;
        let finished = this.state.finished;

        const isValid = this.validateSubmission(response, word_limit);
        if (!isValid) { return; }

        answers[context_number][question_number] = response;

        if (question_number < this.state.questions.length - 1) {
            question_number += 1;
            answers[context_number].push('')
        } else { // we're at the last question
            if (context_number < this.state.contexts.length - 1) {
                context_number += 1;
                question_number = 0;
                answers[context_number] = ['']
            } else { // we're at the last context
                finished = true;
            }
        } 

        this.setState({
            question_number,
            context_number,
            answers,
            finished,
            textInput: '',
        });
    }

    handleStartClick() {
        this.setState({start: false,})
    }

    render() {

        let response;

        if (this.state.story) {
            if (this.state.start) {
                response = (
                    <div className={'start'}>
                        <div>Are you ready?</div>
                        <button onClick={() => this.handleStartClick()}>Start!</button>
                    </div>

                );

            } else if (!this.state.finished) {
                response = (<Question
                    story={this.state.story}
                    context={this.state.contexts[this.state.context_number]}
                    question={this.state.questions[this.state.question_number]['text']}
                    onChange={(e) => this.handleFormChange(e)}
                    onSubmit={(e) => this.handleSubmit(e)}
                    answer={this.state.textInput}
                />);
            } else {
                this.postData();
                response = <div className={'finished'}>
                    Thank you for your time!
                </div>;
            }
        } else {
            response = null;
        }

        return response;
    }
}

export default Study;
