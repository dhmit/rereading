import React from "react";
import PropTypes from 'prop-types';

import {TimeIt} from "../common";
import './reading_view.css';


const segment_ref = React.createRef();
/*
 * Represents the actual Segment window
 */
class Segment extends React.Component {
    constructor(props) {
        super(props);
        // this.segment_div_ref = React.createRef();
    }

    render() {
        const segment_lines = this.props.text.split("\r\n");
        return (
            <div
                className="segment my-3"
                ref={segment_ref}
                onScroll={this.props.handleScroll}
            >
                {segment_lines.map(
                    (line, k) => (<p key={k}>{line}</p>)
                )}
            </div>
        );
    }
}
SegmentQuestion.propTypes = {
    question: PropTypes.object,
    context: PropTypes.object,
    onChange: PropTypes.func,
    onSubmit: PropTypes.func,
    response: PropTypes.string,
};

class ReadingView extends React.Component {
    constructor(props){
        super(props);
        this.state = {
            segment_num: 0,
            timer: null,
            segment_data: [],
            scroll_top: 0,
            scroll_data: [],
            rereading: false,  // we alternate reading and rereading
            document: null,
            interval_timer: null,
            segmentQuestionNum: 0,
            segmentContextNum: 0,
            segmentResponseArray: [],
        };

        this.handleSegmentResponseChange = this.handleSegmentResponseChange.bind(this);
        this.handleSegmentResponseSubmit = this.handleSegmentResponseSubmit.bind(this);
    }

    /**
     * segment_data is an array of arrays. The index of each array
     * corresponds to the segment number of the segments and is updated
     * with new segment data every time the buttons are clicked
     */
    updateData(firstTime){
        if (!firstTime) {
            const segment_data = this.state.segment_data;
            const time = this.state.timer.stop();
            const scroll_data = this.state.scroll_data;
            segment_data.push({
                scroll_data,
                read_time: time,
                is_rereading: this.state.rereading,
                segment_num: this.state.segment_num
            });
            this.setState({segment_data, scroll_data: []});
        }
        const timer = new TimeIt();
        this.setState({timer});
    }

    // We have the big arrow notation here to bind "this" to this function
    handleScroll = (e) => {
        const scroll_top = e.target.scrollTop;
        this.setState({scroll_top});
    };

    recordScroll = () => {
        const scroll_data = this.state.scroll_data;
        scroll_data.push(this.state.scroll_top);
        this.setState({scroll_data});
    };

    async componentDidMount() {
        try {
            // Hardcode the document we know exists for now,
            // Generalize later...
            const response = await fetch('/api/documents/1');
            const document = await response.json();
            const interval_timer = setInterval(this.recordScroll, 2000);
            this.setState({document, interval_timer});
            this.updateData(true);
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

    prevSegment () {
        this.updateData(false);
        // document will be replaced by actual data
        if (this.state.segmentNum > 0){
            this.setState({
                segmentNum: this.state.segmentNum-1,
                rereading: true,
                segmentQuestionNum: 0,
                segmentContextNum: 0,
            });
        }
        segment_ref.current.scrollTo(0,0);

    }

    nextSegment () {
        this.updateData(false);
        const length = this.state.document.segments.length;
        const current_segment = this.state.segmentNum;
        if (current_segment < length){
            if (this.state.rereading) {

                // Copy the response array to prevent weird shenanigans
                const segmentResponseArray = this.state.segmentResponseArray.slice();

                const segment_questions = this.state.document.segments[current_segment].questions;
                const num_segment_questions = segment_questions.length;
                segmentResponseArray.push(Array(num_segment_questions));

                // If we're already rereading, move to the next segment
                this.setState({
                    rereading: false,
                    segmentNum: this.state.segmentNum+1,
                    segmentQuestionNum: 0,
                    segmentContextNum: 0,
                    segmentResponseArray,
                });
            } else {
                // Otherwise, move on to the rereading layout
                this.setState({rereading: true});
            }
        }

        segment_ref.current.scrollTo(0,0);
    }

    /**
     * Handles data when a user is trying to submit a response to a question
     */
    handleSegmentResponseSubmit(event) {
        event.preventDefault();
    }

    buildQuestionFields(questions, context_text) {
        return questions.map((question, id) => (
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
        ))
    }

    render() {
        const data = this.state.document;

        if (data) {
            const current_segment = data.segments[this.state.segmentNum];
            const segment_text = current_segment.text;
            const segment_questions = current_segment.questions;

            const segment_contexts = current_segment.contexts;
            const current_context = (this.segmentContextNum < segment_contexts.length) ?
                segment_contexts[this.segmentContextNum].text : 'No segment context given';

            // Generate response fields for each of the questions
            const segment_response_fields = this.buildQuestionFields(segment_questions,
                current_context);

            return (
                <div className={"container"}>
                    <h1 className={"display-4 py-3 pr-3"}>{data.title}</h1>
                    <div className={"row"}>
                        <div className={'col-8'}>
                            <p>Segment Number: {this.state.segment_num + 1}</p>
                            <Segment
                                text={segment_text}
                                handleScroll={(e) => this.handleScroll(e)}
                            />
                            <button
                                className={"btn btn-outline-dark mr-2"}
                                onClick={() => this.prevSegment()}
                            >
                                Back
                            </button>

                            <button
                                className={"btn btn-outline-dark"}
                                onClick = {() => this.nextSegment()}
                            >
                                {this.state.rereading ? 'Next' : 'Reread'}
                            </button>
                        </div>

                        {this.state.rereading &&
                            <div className={"analysis col-4"}>
                                {segment_response_fields}
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
