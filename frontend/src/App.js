import React from 'react';
import './App.css';
import Button from 'react-bootstrap/Button'

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
        <div className={'question'}>
            <div className={'question-prompt'}>{props.question}</div>
            <form onSubmit={props.onSubmit}>
                <label>
                    <input type={'text'} value={props.answer} onChange={props.onChange} />
                </label>
                <div>
                    <Button variant='primary' type='submit' size='lg' block>Continue</Button>
                </div>
            </form>
            <Button variant='secondary' onClick={props.goBack}>Go back to story</Button>
        </div>
    );
}

function Story(props) {
    return (
        <div className={'story'}>
            <div className={'context-text'}>{props.context}</div>
            <div className={'story-text'}>{props.story}</div>
            <button onClick={props.onClick}>Continue</button>
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
            answers: [],
            finished: false,
            start: true,
            textInput: '',
            views: 0,
            show_story: true,
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
        const url = 'http://localhost:8000/api/add-response/';
        const data = {
            story: this.state.story,
            student_responses: this.state.answers,
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
                alert('Make sure to respect word limits.');
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
        let views = this.state.views;
        const word_limit = this.state.questions[question_number].word_limit;
        let finished = this.state.finished;
        let show_story = this.state.show_story;

        const isValid = this.validateSubmission(response, word_limit);
        if (!isValid) { return; }

        // answers[context_number][question_number] = response;
        const answer = {
            'context': this.state.contexts[context_number],
            'question': this.state.questions[question_number].text,
            response,
            views,
        };
        answers.push(answer);
        views = 0;

        if (question_number < this.state.questions.length - 1) {
            question_number += 1;

        } else { // we're at the last question
            if (context_number < this.state.contexts.length - 1) {
                context_number += 1;
                question_number = 0;
                show_story = true;
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
            show_story,
            views,
        });
    }

    handleStartClick() {
        this.setState({start: false,})
    }

    toggleStory() {
        const show_story = !this.state.show_story;
        let views = this.state.views;
        if (show_story) {
            views++;
        }
        this.setState({
            show_story,
            views,
        });
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
                if (this.state.show_story) {
                    response = (<Story
                        story={this.state.story}
                        context={this.state.contexts[this.state.context_number]}
                        onClick={() => this.toggleStory()}
                    />);
                } else {
                    response = (<Question
                        story={this.state.story}
                        context={this.state.contexts[this.state.context_number]}
                        question={this.state.questions[this.state.question_number]['text']}
                        onChange={(e) => this.handleFormChange(e)}
                        onSubmit={(e) => this.handleSubmit(e)}
                        answer={this.state.textInput}
                        goBack={() => this.toggleStory()}
                    />);
                }
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

