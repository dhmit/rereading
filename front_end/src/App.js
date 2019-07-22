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
            </form>
            <button onClick={props.onSubmit}>{'Continue'}</button>
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
            is_start: true,
            answers: [[]],
            finished: false,
            start: true,
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

    handleFormChange(e) {
        const context = this.state.context_number;
        const question = this.state.question_number;
        const responses = this.state.answers.slice();

        if (responses[context]) {
            responses[context][question] = e.target.value;
        } else {
            responses[context] = [e.target.value];
        }

        this.setState({answers: responses});

    }

    handleSubmit(e) {
        e.preventDefault();
        let question_number = this.state.question_number;
        let new_context = this.state.context_number;
        let answers = this.state.answers.slice();
        let finished = false;
        let response = answers[new_context][question_number];
        let word_limit = this.state.questions[question_number].word_limit;
        if (!response) {
            alert('Please enter a response.');
            return null;
        }
        question_number += 1;

        const response_list = response.split(' ');

        if (response_list.length <= word_limit) {
            if (question_number === this.state.questions.length) {
                new_context += 1;
                question_number = 0;
                answers[new_context] = [];
            }

            if (new_context === this.state.contexts.length) {
                finished = true;
                answers = answers.slice(0, new_context)
            }

            this.setState({
            question_number: question_number,
            context_number: new_context,
            answers: answers,
            finished: finished,
            });

            e.target.reset();

        } else {
            alert('Make sure to respect word limits.')
        }
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

            } else if (!this.state.finished && this.state.question_number) {
                response = (<Question
                    story={this.state.story}
                    context={this.state.contexts[this.state.context_number]}
                    question={this.state.questions[this.state.question_number]['text']}
                    onChange={(e) => this.handleFormChange(e)}
                    onSubmit={(e) => this.handleSubmit(e)}
                    answer={this.state.answers[this.state.context_number][this.state.question_number]}
                />);
            } else {
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
