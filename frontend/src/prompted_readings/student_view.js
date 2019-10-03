import React from 'react';
import PropTypes from 'prop-types';

import { getCookie } from '../common'
import './student_view.css';


/**
 * This is used as a helper function for keeping track of
 * how long a user has been looking at a story
 */
class TimeIt {
    constructor() {
        this.start = Date.now();
        this.end = null;
        this.time = 0;
    }

    /**
     * This stops the timer and logs how long the timer has been running
     *
     * TODO: ensure that the timer has been running,
     * and that you are not calling stop() back to back
     */
    stop() {
        this.end = Date.now();
        this.time += this.end - this.start;
        return this.time / 1000;
    }

    /**
     * Restarts the timer while maintaining the current time that was stored,
     * useful for when someone takes a break or is no longer looking at the proper page
     */
    // noinspection JSUnusedGlobalSymbols
    resume() {
        this.start = Date.now();
    }
}

TimeIt.propTypes = {
    onScroll: PropTypes.func,
    onSubmit: PropTypes.func,
    onChange: PropTypes.func,
    answer: PropTypes.string,
    word_limit: PropTypes.number
};


/**
 * That big fancy blue button at the bottom of the screen, progresses the user to the next page
 */
function ContinueBtn(props) {
    return (
        <nav className="navbar fixed-bottom">
            <button className="btn btn-primary btn-lg btn-block" onClick={props.onClick}>
                Continue
            </button>
        </nav>
    );
}

ContinueBtn.propTypes = {
    onClick: PropTypes.func
};


/**
 * Displays the question page to the user, including all relevant progression features
 */
function Question(props) {
    return (
        <div className={'question'}>
            <div className={'question-prompt'}>{props.question}</div>
            <ContinueBtn onClick={props.onClick}/>
        </div>
    );
}

Question.propTypes = {
    question: PropTypes.string,
    onClick: PropTypes.func,
};


/**
 * Displays the story page to the user.
 *
 * The story itself is located in a div that tracks when and how the user scrolls.
 *
 * Also contains progression features for moving to the next page
 */
function Story(props) {
    return (
        <div className='story'>
            <div className={'story-box'} onScroll={props.onScroll}>
                <div className={'story-text'}>{props.story_text}</div>
            </div>
            <ContinueBtn onClick={props.onClick}/>
        </div>
    );
}
Story.propTypes = {
    story_text: PropTypes.string,
    onScroll: PropTypes.func,
    onClick: PropTypes.func,
};


/**
 * Displays the context page to the user, including all relevant progression features
 */
function Context(props) {
    return (
        <div className='context'>
            <div className={'context-text'}>{props.context}</div>
            <ContinueBtn onClick={props.onClick}/>
        </div>
    );
}
Context.propTypes = {
    context: PropTypes.string,
    onClick: PropTypes.func,
};


/**
 * Page that handles letting the user submit responses.
 *
 * Allows the user to
 *      - go back to view the story/question/etc. if they want to see it again or
 *      - continue once they have a response
 */
function Response(props) {
    return (
        <div className='response'>
            <form onSubmit={props.onSubmit}>
                <div className='form-group'>
                    <label className="form-control">{props.question}</label>
                    <input
                        type='text' className="form-control"
                        onChange={props.onChange} value={props.answer}
                    />
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
Response.propTypes = {
    question: PropTypes.string,
    answer: PropTypes.string,
    onSubmit: PropTypes.func,
    onChange: PropTypes.func,
    onScroll: PropTypes.func,
    goBack: PropTypes.func,
};


/**
 * Displays a page allowing the user to go back and see the sequence of prompts again
 * should they need it, or move on if they feel they understand
 */
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
GoBack.propTypes = {
    continue: PropTypes.func,
    goBack: PropTypes.func,
};


/**
 * Displays an error message if the user did not follow the guidelines for a response
 *
 * @return {null}
 */
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


/**
 * Main component for the student view.
 *
 * Handles all logic, displays information, and makes database query/posts
 */
class StudentView extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            story_text: null,
            contexts: [],
            questions: [],
            context_number: 0,
            question_number: 0,
            answers: [],
            finished: false,
            textInput: '',
            views: '[]', // views is stored as a json string due to Django constraints
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
        this.csrftoken = getCookie('csrftoken');
    }

    /**
     * Grabs relevant story information from the server and stores it for displaying later
     */
    async componentDidMount() {
        try {
            const questions = await fetch('/api/');
            const json = await questions.json();
            // TODO: (?) Currently only accesses first story, cannot handle multiple
            this.setState(json[0]);
        } catch (e) {
            console.log(e);
        }
    }

    /**
     * Once the user has finished answering all of the questions,
     * this function uploads all of the data to the database
     * so that it can be referenced in the instructor view
     */
    postData() {
        const url = '/api/add-response/';
        const data = {
            story_text: this.state.story_text,
            student_responses: this.state.answers,
        };

        console.log(JSON.stringify(data));

        fetch(url, {
            method: 'POST',
            body: JSON.stringify(data),
            headers: {
                'Content-type': 'application/json',
                'X-CSRFToken': this.csrftoken,
            }

        }).then(res => res.json()).then(response => console.log(JSON.stringify(response)))
            .catch(err => console.log(err));
    }

    /**
     * Called when the user provides input into the response field,
     * and updates the state accordingly
     */
    handleFormChange(e) {
        this.setState({textInput: e.target.value});
    }


    /**
     * Ensures that the response the user is trying to submit
     * obeys the word limit (as well as check that the response exists).
     *
     * Returns false if there is a conflict between the rules and response, true otherwise
     */
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


    /**
     * When a user tries to submit a response, this function should be called.
     *
     * It first checks to make sure that the response is valid
     * and then stores it in memory in a format that is easy to transfer
     * to Django when the user has completed all of the questions
     */
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

        // Don't let the user submit until their response fits the criteria of the question
        const isValid = StudentView.validateSubmission(response, word_limit);
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
        views = '[]';  // Reset views for the next response
        const timer = new TimeIt();  // Refresh the timer so that you aren't double counting
        scroll_ups = 0;  // Reset scrolls for next response

        // Logic for storing data in memory
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

    /**
     * Readies all information for when the user presses the start button on the landing screen
     */
    handleStartClick() {
        const timer = new TimeIt();
        this.setState({show_story: true, timer,});
    }

    /**
     * Handles what to do when the user advances past the story page
     */
    storyButtonClick() {
        // Keep track of the length of time that the user viewed the story
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

    /**
     * Handles what to do when the user advances past the context page
     */
    contextButtonClick() {
        this.setState({show_context: false, show_question:true});
    }

    /**
     * Handles what to do when the user advances past the question page
     */
    questionButtonClick() {
        this.setState({show_question: false, show_go_back: true,});
    }

    /**
     * When the user presses a back button, displays the relevant page and starts a new timer object
     */
    backButtonClick() {
        const timer = new TimeIt();
        this.setState({
            show_go_back: false,
            show_story: true,
            show_response: false,
            timer,
        });
    }

    /**
     * Handles what to do when the user advances beyond the page that checks if they wish to go back
     */
    continueButtonClick() {
        this.setState({show_go_back: false, show_response:true});
    }

    /**
     * For large enough stories, this function logs how many times the user scrolls up to
     * read a previous portion of the story
     *
     * Note: This only tracks the number of times scrolled up, and not when the user scrolls
     * down to "advance" the story
     */
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

        if (this.state.story_text) { // Check that the story is loaded before showing any data
            if (this.state.show_story) {
                response = (
                    <Story
                        story_text={this.state.story_text}
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
                            <button
                                className="btn btn-primary btn-lg btn-block"
                                onClick={() => this.handleStartClick()}>
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

export default StudentView;

