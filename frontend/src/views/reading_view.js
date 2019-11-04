import React from "react";
import {TimeIt, handleStoryScroll} from "../common";
import './reading_view.css';
import PropTypes from 'prop-types';

class Segment extends React.Component {
    render() {
        return (
            <div className="scroll">
                <p>Segment Number: {this.props.segment_num + 1}</p>
                {this.props.segmentLines.map((line, k) => (
                    <p key={k}>{line}</p>)
                )}
            </div>
        )
    }
}
Segment.propTypes = {
    segmentLines: PropTypes.array,
    segment_num: PropTypes.number,
};


class ReadingView extends React.Component {
    constructor(props){
        super(props);
        this.state = {
            segment_num: 0,
            timer: null,
            segment_data: [],
            scrollTop: 0,
            scroll_ups: 0,
            scrolling_up: false,
            rereading: false,  // we alternate reading and rereading
            document: null,
            segmentQuestionNum: 0,
            segmentContextNum: 0,
            segmentResponseArray: [],
        };

        this.handleSegmentResponseChange = this.handleSegmentResponseChange.bind(this);
        this.handleSegmentResponseSubmit = this.handleSegmentResponseSubmit.bind(this);
    }

    /**
     * segment_read_times is a array of arrays. The index of each array
     * corresponds to the segment number of the segments and is updated
     * with a new time every time the buttons are clicked
     */
    updateData(firstTime){
        if (!firstTime) {
            const segment_data = this.state.segment_data;
            const time = this.state.timer.stop();
            segment_data.push({
                scroll_ups: this.state.scroll_ups,
                read_time: time,
                is_rereading: this.state.rereading,
                segment_num: this.state.segment_num
            });
            this.setState({segment_data, scroll_ups: -1});
        }
        const timer = new TimeIt();
        this.setState({timer});
    }

    // We have the big arrow notation here to bind "this" to this function
    handleScroll = (e) => {
        this.setState(handleStoryScroll(e, this.state.scrollTop, this.state.scroll_ups,
            this.state.scrolling_up));
    };

    prevSegment () {
        this.updateData(false);
        this.setState({segment_num: this.state.segment_num-1});
        window.scrollTo(0,0);
    }

    nextSegment () {
        this.updateData(false);
        if (this.state.rereading) {
            // If we're already rereading, move to the next segment
            this.setState({rereading: false, segment_num: this.state.segment_num+1});
        } else {
            // Otherwise, move on to the rereading layout
            this.setState({rereading: true});
        }
        window.scrollTo(0,0);
    }

    async componentDidMount() {
        try {
            // Hard code the document we know exists for now,
            // Generalize later...
            const response = await fetch('/api/documents/1');
            const document = await response.json();
            this.setState({document});
            this.updateData(true);
            // This will allow the scroll detector to work
            /** TODO: Add event listener to the reading pane when it is complete to track scroll
             *        data on that reading pane only. Currently, it is tracking scrolling data
             *        for entire page
             */
            window.addEventListener('scroll', this.handleScroll, true);
        } catch (e) {
            console.log(e);
        }

    }

    /**
     * Allows the user to change their response to a segment question
     */
    handleSegmentResponseChange(question_id, event) {
        const segmentResponseArray = this.state.segmentResponseArray.slice();

        let question_entry = null;
        for (let el of segmentResponseArray) {
            if (el.id === question_id) {
                question_entry = el;
                break;
            }
        }

        if (question_entry === null) {
            question_entry = {id: question_id};
            segmentResponseArray.push(question_entry);
        }

        question_entry.response = event.target.value;

        this.setState({segmentResponseArray});

    }

    /**
     * Handles data when a user is trying to submit a response to a question
     */
    handleSegmentResponseSubmit(event) {
        event.preventDefault();
    }


    render() {
        const doc = this.state.document;

        if (doc) {
            const current_segment = doc.segments[this.state.segment_num];
            const segment_text = current_segment.text;
            const segment_lines = segment_text.split("\r\n");
            const segment_questions = current_segment.questions;

            // const segment_contexts = current_segment.contexts;
            const context_text = "Example context text";

            // Generate response fields for each of the questions
            const response_fields = segment_questions.map((question, id) => {
                return (
                    <React.Fragment key={id}>
                        <div>
                            <h4>Context:</h4>
                            <div className='segment-context-text'>
                                {context_text}
                            </div>
                            <h4>Question:</h4>
                            <div className='segment-question-text'>
                                {question.text}
                            </div>

                            <label><h4>Response:</h4></label>
                            <input
                                type='text'
                                onChange={this.handleSegmentResponseChange.bind(this,
                                    question.id)}
                            />

                        </div>
                    </React.Fragment>
                )
            });

            return (
                <div className={"container"}>
                    <h1 className={"display-4 py-3 pr-3"}>{doc.title}</h1>
                    <div className={"row"}>
                        <Segment
                            segmentLines={segment_lines}
                            segment_num={this.state.segment_num}
                        />
                        <div className={'col-8'}>
                            <button
                                className={"btn btn-outline-dark mr-2"}
                                onClick={() => this.prevSegment()}
                            >
                                Back
                            </button>
                            <button
                                className={"btn btn-outline-dark"}
                                onClick={() => this.nextSegment()}
                            >
                                {this.state.rereading ? 'Next' : 'Reread'}
                            </button>
                        </div>

                        {this.state.rereading &&
                            <div className={"analysis col-4"}>
                                {response_fields}
                            </div>
                        }
                    </div>
                </div>
            );
        } else {
            return (
                <div>Loading!</div>
            );
        }

    }
}

export default ReadingView;
