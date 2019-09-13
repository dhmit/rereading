import React from 'react';
import './student_view.css';
import PropTypes from 'prop-types';

class TimeIt {
    constructor() {
        this.start = Date.now();
        this.end = null;
        this.time = 0;
    }

    stop() {
        this.end = Date.now();
        this.time += this.end - this.start;
        return this.time / 1000;
    }

    // noinspection JSUnusedGlobalSymbols
    resume() {
        this.start = Date.now();
    }
}

function ContinueBtn(props) {
    return (
        <nav className="navbar fixed-bottom">
            <button className="btn btn-primary btn-lg btn-block" onClick={props.onClick}>Continue</button>
        </nav>
    );
}

function Question(props) {
    return (
        <div className={'question'}>
            <div className={'question-prompt'}>{props.question}</div>
            <ContinueBtn onClick={props.onClick}/>
        </div>
    );
}

TimeIt.propTypes = {
    onScroll: PropTypes.func,
    onSubmit: PropTypes.func,
    onChange: PropTypes.func,
    answer: PropTypes.string,
    word_limit: PropTypes.number
};

function Story(props) {
    return (
        <div className='story'>
            <div className={'story-box'} onScroll={props.onScroll}>
                <div className={'story-text'}>{props.story}</div>
            </div>
            <ContinueBtn onClick={props.onClick}/>
        </div>
    );
}

function Context(props) {
    return (
        <div className='context'>
            <div className={'context-text'}>{props.context}</div>
            <ContinueBtn onClick={props.onClick}/>
        </div>
    );
}

function Response(props) {
    return (
        <div className='response'>
            <form onSubmit={props.onSubmit}>
                <div className='form-group'>
                    <label className="form-control">{props.question}</label>
                    <input type='text' className="form-control" onChange={props.onChange} value={props.answer} />
                </div>
                <nav className="navbar fixed-bottom">
                    <div className='btn-group btn-group-lg multi-button'>
                        <button className='btn btn-secondary' type='submit'>Submit</button>
                        <button className='btn btn-primary' onClick={props.goBack}>Go Back</button>
                    </div>
                </nav>
            </form>
        </div>
    );
}

function GoBack(props) {
    return (
        <div className='go-back'>
            <div>Would you like to see that again?</div>
            <nav className="navbar fixed-bottom">
                <div className='btn-group btn-group-lg multi-button'>
                    <button className='btn btn-secondary' onClick={props.continue}>No</button>
                    <button className='btn btn-primary' onClick={props.goBack}>Yes</button>
                </div>
            </nav>
        </div>
    );
}

function WordAlert(props) {
    if (props.word_alert) {
        return (
            <div className='word-alert'>
                <div className='alert alert-danger' role='alert'>
                    Please make sure to enter a response and respect word limits
                </div>
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
            views: '[]', // views is stored as a json string
            show_story: false,
            show_context: false,
            show_question: false,
            show_response: false,
            show_go_back: false,
            word_alert: false,
            timer: null,
            scrollTop: 0,
            scroll_ups: 0,
            scrolling_up: false,
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

    static validateSubmission(response, word_limit) {
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
        let scroll_ups = this.state.scroll_ups;

        const isValid = Study.validateSubmission(response, word_limit);
        if (!isValid) {
            this.setState({word_alert: true,});
            return;
        }

        const answer = {
            'context': this.state.contexts[context_number],
            'question': this.state.questions[question_number].text,
            response,
            views,
            scroll_ups,
        };
        answers.push(answer);
        views = '[]'; // Reset views for the next response
        const timer = new TimeIt(); // Refresh the timer so that you aren't double counting
        scroll_ups = 0;

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
            timer,
            scroll_ups,
        });
    }

    handleStartClick() {
        const timer = new TimeIt();
        this.setState({show_story: true, timer,});
    }

    storyButtonClick() {
        const view_list = JSON.parse(this.state.views);
        const time = this.state.timer.stop();
        view_list.push(time);
        const views = JSON.stringify(view_list);
        this.setState({
            show_story: false,
            show_context:true,
            views,
        });
    }

    contextButtonClick() {
        this.setState({show_context: false, show_question:true});
    }

    questionButtonClick() {
        this.setState({show_question: false, show_go_back: true,});
    }

    backButtonClick() {
        const timer = new TimeIt();
        this.setState({
            show_go_back: false,
            show_story: true,
            show_response: false,
            timer,
        });
    }

    continueButtonClick() {
        this.setState({show_go_back: false, show_response:true});
    }

    handleStoryScroll(e) {
        const scrollTop = e.target.scrollTop;
        const prev_scroll = this.state.scrollTop;
        let scroll_ups = this.state.scroll_ups;
        let scrolling_up = this.state.scrolling_up;

        // If the user is scrolling up, log it
        if (scrollTop < prev_scroll && !scrolling_up) {
            scroll_ups++;
            scrolling_up = true;
        } else if (scrollTop > prev_scroll && scrolling_up) {
            scrolling_up = false;
        }

        this.setState({scrollTop, scroll_ups, scrolling_up});
    }


    render() {

        let response;

        if (this.state.story) {
            if (this.state.show_story) {
                response = (<Story
                        story={this.state.story}
                        onClick={() => this.storyButtonClick()}
                        onScroll={(e) => this.handleStoryScroll(e)}
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
                            goBack={() => this.backButtonClick()}
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
                        <nav className="navbar fixed-bottom">
                            <button className="btn btn-primary btn-lg btn-block" onClick={() => this.handleStartClick()}>
                                Start!
                            </button>
                        </nav>
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

