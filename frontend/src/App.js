import React from 'react';
import './App.css';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import Alert from 'react-bootstrap/Alert';
import Navbar from 'react-bootstrap/Navbar';


function Question(props) {
    return (
        <div className={'question'}>
            <div className={'question-prompt'}>{props.question}</div>
            <Navbar fixed={'bottom'}>
                <Button variant='primary' onClick={props.onClick} size='lg' block>Continue</Button>
            </Navbar>
        </div>
    );
}

function Story(props) {
    return (
        <div className='story'>
            <div className={'story-text'}>{props.story}</div>
            <Navbar fixed={'bottom'}>
                <Button variant='primary' onClick={props.onClick} size='lg' block>Continue</Button>
            </Navbar>
        </div>
    );
}

function Context(props) {
    return (
        <div className='context'>
            <div className={'context-text'}>{props.context}</div>
            <Navbar fixed='bottom'>
                <Button variant='primary' onClick={props.onClick} size='lg' block>Continue</Button>
            </Navbar>
        </div>
    )
}

function Response(props) {
    return (
        <div className='response'>
            <Form onSubmit={props.onSubmit}>
                <Form.Group>
                    <Form.Label>{props.question}</Form.Label>
                    <Form.Control type='text' onChange={props.onChange} value={props.answer} />
                </Form.Group>
                <Navbar fixed='bottom'>
                    <Button variant='primary' type='submit' size='lg' block>Submit</Button>
                </Navbar>
            </Form>
        </div>
    );
}

function GoBack(props) {
    return (
        <div className='go-back'>
            <div>Would you like to see that again?</div>
            <Navbar fixed='bottom'>
                <Button variant='primary' onClick={props.goBack} size='lg' block>Yes</Button>
                <Button variant='secondary' onClick={props.continue} size='lg' block>No</Button>
            </Navbar>
        </div>
    );
}

function WordAlert(props) {

    if (props.word_alert) {
        return (
            <div className='word-alert'>
                <Alert variant='danger'>
                    Please make sure to enter a response and respect word limits
                </Alert>
            </div>
        );
    } else {
        return null;
    }
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
            textInput: '',
            views: 1,
            show_story: false,
            show_context: false,
            show_question: false,
            show_response: false,
            show_go_back: false,
            word_alert: false,
        };

    }

    async componentDidMount() {
        // Load from server

        try {
            const questions = await fetch('/api/');
            const json = await questions.json();
            this.setState(json[0]);
        } catch (e) {
            console.log(e);
        }

        // this.setState(list[0])
    }

    postData() {
        const url = '/api/add-response/';
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
            return false;
        } else {
            const response_list = response.trim().split(' ');
            if (!(response_list.length <= word_limit)) {
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
        let show_response = this.state.show_response;

        const isValid = this.validateSubmission(response, word_limit);
        if (!isValid) {
            this.setState({word_alert: true,});
            return;
        }

        const answer = {
            'context': this.state.contexts[context_number],
            'question': this.state.questions[question_number].text,
            response,
            views,
        };
        answers.push(answer);
        views = 1;

        if (question_number < this.state.questions.length - 1) {
            question_number += 1;

        } else { // we're at the last question
            if (context_number < this.state.contexts.length - 1) {
                context_number += 1;
                question_number = 0;
                show_story = true;
            } else { // we're at the last context
                finished = true;
                show_story = false;
                show_response = false;
            }
        }

        this.setState({
            question_number,
            context_number,
            answers,
            finished,
            textInput: '',
            show_story,
            show_response,
            views,
            word_alert: false,
        });
    }

    handleStartClick() {
        this.setState({show_story: true,})
    }

    storyButtonClick() {
        this.setState({show_story: false, show_context:true,})
    }

    contextButtonClick() {
        this.setState({show_context: false, show_question:true})
    }

    questionButtonClick() {
        this.setState({show_question: false, show_go_back: true,})
    }

    backButtonClick() {
        this.setState({show_go_back: false, show_story: true,})
    }

    continueButtonClick() {
        this.setState({show_go_back: false, show_response:true})
    }


    render() {

        let response;

        if (this.state.story) {
            if (this.state.show_story) {
                response = (<Story
                        story={this.state.story}
                        onClick={() => this.storyButtonClick()}
                    />
                );
            } else if (this.state.show_context) {
                response = (
                    <Context
                        context={this.state.contexts[this.state.context_number]}
                        onClick={() => this.contextButtonClick()}
                    />
                );
            } else if (this.state.show_go_back) {
                response = (
                    <GoBack
                        goBack={() => this.backButtonClick()}
                        continue={() => this.continueButtonClick()}
                    />
                );
            } else if (this.state.show_question) {
                response = (
                    <Question
                        question={this.state.questions[this.state.question_number]['text']}
                        onClick={() => this.questionButtonClick()}
                    />
                );
            } else if (this.state.show_response) {
                response = (
                    <div>
                        <WordAlert word_alert={this.state.word_alert}/>
                        <Response
                            onSubmit={(e) => this.handleSubmit(e)}
                            onChange={(e) => this.handleFormChange(e)}
                            question={this.state.questions[this.state.question_number]['text']}
                            answer={this.state.textInput}
                        />
                    </div>
                );
            } else if (this.state.finished) {
                this.postData();
                response = (
                    <div className={'finished'}>
                        Thank you for your time!
                    </div>
                );
            } else {
                response = (
                    <div className={'start'}>
                        <div>Are you ready?</div>
                        <Navbar fixed={'bottom'}>
                            <Button variant='primary' onClick={() => this.handleStartClick()} size='lg' block>
                                Start!
                            </Button>
                        </Navbar>
                    </div>
                );
            }
        } else { // Haven't pulled prompts from database yet
            response = null;
        }

        return response;
    }
}

export default Study;

