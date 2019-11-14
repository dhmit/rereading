import React from "react";
import PropTypes from 'prop-types';

import {getCookie, TimeIt} from "../common";
import './reading_view.css';


/*
 * Represents the actual Segment window
 */
class Segment extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        const segment_lines = this.props.text.split("\r\n");
        return (
            <div
                className="segment my-3"
                ref={this.props.segment_ref}
                onScroll={this.props.handleScroll}
            >
                {segment_lines.map(
                    (line, k) => (<p key={k}>{line}</p>)
                )}
            </div>
        );
    }
}
Segment.propTypes = {
    text: PropTypes.string,
    handleScroll: PropTypes.func,
    segment_ref: PropTypes.shape({current: PropTypes.instanceOf(Element)})
};


class OverviewWindow extends React.Component {
    render() {
        const full_document_text = [];
        this.props.all_segments.map((el) => full_document_text.push(el.text.split("\r\n")));
        return (
            <div className={"row"}>
                <div className={"col-8"}>
                    <div className="scroll_overview">
                        {full_document_text.map((segment_text_array) => (
                            segment_text_array.map((text,i) => (
                                <p key={i}>{text}</p>
                            ))
                        ))}
                    </div>
                </div>
                <div className={"col-4"}>
                    <p><b>Document Questions</b></p>
                    {this.props.document_questions.map((el, i) => (
                        <p key={i}>{el.is_overview_question ? null : el.text}</p>)
                    )}
                    <p><b>Overview Questions</b></p>
                    {this.props.document_questions.map((el, i) => (
                        <p key={i}>{el.is_overview_question ? el.text : null}</p>)
                    )}
                </div>
            </div>
        );
    }
}
OverviewWindow.propTypes = {
    all_segments: PropTypes.array,
    document_questions: PropTypes.array,
};


class ReadingView extends React.Component {
    constructor(props){
        super(props);
        this.state = {
            segment_num: 0,
            timer: null,
            scroll_top: 0,
            scroll_data: [],
            segments_viewed: [0],
            jump_to_value: null,
            rereading: false,  // we alternate reading and rereading
            document: null,
            interval_timer: null,
            segmentQuestionNum: 0,
            segmentResponseArray: [],
            student_id: 15, //temporary
        };
        this.csrftoken = getCookie('csrftoken');

        this.segment_ref = React.createRef();
        this.handleSegmentResponseChange = this.handleSegmentResponseChange.bind(this);
    }

    async componentDidMount() {
        try {
            // Hard code the document we know exists for now -- generalize later...
            const response = await fetch('/api/documents/1');
            const document = await response.json();
            const interval_timer = setInterval(() => this.recordScroll(), 2000);
            this.setState({document, interval_timer});
            this.sendData(true);
        } catch (e) {
            console.log(e);
        }
    }

    /**
     * segment_data is an array of arrays. The index of each array
     * corresponds to the segment number of the segments and is updated
     * with new segment data every time the buttons are clicked
     */
    sendData(firstTime){
        if (!firstTime && this.state.rereading) {
            const time = this.state.timer.stop();
            this.setState({scroll_data: []});
            const url = '/api/add-response/';
            const reading_data = {
                reading_data_id: this.state.document.new_reading_data_id,
                segment_responses: this.state.segmentResponseArray,
                segment_data: [{
                    id: this.state.document.segments[this.state.segment_num].id,
                    scroll_data: JSON.stringify(this.state.scroll_data),
                    view_time: time,
                    is_rereading: this.state.rereading,
                }],
            };
            fetch(url, {
                method: 'POST',
                body: JSON.stringify(reading_data),
                headers: {
                    'Content-type': 'application/json',
                    'X-CSRFToken': this.csrftoken,
                }

            }).then(res => res.json()).then(response => console.log(JSON.stringify(response)))
                .catch(err => console.log(err));
        }
        const timer = new TimeIt();
        this.setState({timer});
    }

    recordScroll() {
        const scroll_data = this.state.scroll_data;
        scroll_data.push(this.state.scroll_top);
        this.setState({scroll_data});
    }

    handleScroll(e) {
        const scroll_top = e.target.scrollTop;
        this.setState({scroll_top});
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
        this.sendData(false);
        this.gotoSegment(this.state.segment_num - 1);
        this.segment_ref.current.scrollTo(0,0);
    }

    nextSegment () {
        this.sendData(false);

        if (this.state.rereading) {
            // If we're already rereading, move to the next segment
            this.gotoSegment(this.state.segment_num + 1);
            this.setState({segmentResponseArray: []})
            //TODO Figure out if this can be integrated into gotoSegment. I wasn't exactly
            // sure why it was being set here but not prevSegment().
        } else {
            // Otherwise, move on to the rereading layout
            this.setState({rereading: true});
        }

        this.segment_ref.current.scrollTo(0,0);
    }

    gotoSegment(segmentNum) {
        let segmentCount = this.state.document.segments.length;
        if (segmentNum >= 0 && segmentNum < segmentCount) {
            const segments_viewed = this.state.segments_viewed.slice();
            let rereading = segments_viewed.includes(segmentNum);

            //The segment number is pushed regardless of whether or not the user has read the page
            // before so that page reread order can also be determined.
            segments_viewed.push(segmentNum);
            this.setState({
                rereading,
                segments_viewed,
                segment_num: segmentNum,
                segmentQuestionNum: 0,
            });
        }
    }

    handleJumpToFieldChange = (e) => {
        let numericValue = parseInt(e.target.value) - 1;
        this.setState({jump_to_value: numericValue});
    };

    handleJumpToButton = () => {
        this.gotoSegment(this.state.jump_to_value);
    };

    toOverview () {
        this.setState({overview: true})
    }

    buildQuestionFields(questions) {
        return questions.map((question, id) => (
            <React.Fragment key={id}>
                <div className="mb-2">
                    <div className='segment-question-text'>
                        {question.text}
                    </div>
                    <textarea
                        className={'form-control'}
                        onChange={
                            this.handleSegmentResponseChange.bind(this, question.id)
                        }
                    />

                </div>
            </React.Fragment>
        ))
    }

    render() {
        const doc = this.state.document;
        if (!doc) {
            return (
                <div>Loading!</div>
            );
        }
        const current_segment = doc.segments[this.state.segment_num];
        const segment_questions = current_segment.questions;

        // Generate response fields for each of the questions
        const segment_response_fields = this.buildQuestionFields(segment_questions);

        const document_questions = doc.questions;

        return (
            <div className={"container"}>
                <h1 className={"display-4 py-3 pr-3"}>{doc.title}</h1>

                {this.state.overview ?
                    <OverviewWindow
                        all_segments={doc.segments}
                        document_questions={document_questions}
                    />
                    :
                    <React.Fragment>
                        <div className={"row"}>
                            <div className={'col-8'}>
                                <p>Segment Number: {this.state.segment_num + 1}</p>
                                <Segment
                                    text={current_segment.text}
                                    handleScroll={(e) => this.handleScroll(e)}
                                    segment_ref={this.segment_ref}
                                />
                            </div>

                            {this.state.rereading &&
                                <div className={"analysis col-4"}>
                                    {segment_response_fields}

                                    {document_questions && (
                                        <div>
                                            <p><b>Document Questions: </b></p>
                                            {document_questions.map((el,i) =>
                                                <p key={i}>
                                                    {el.is_overview_question ? null : el.text}
                                                </p>
                                            )}
                                        </div>
                                    )}
                                </div>
                            }
                        </div>
                        <div className={"row"}>
                            <div className={"col-4"}>
                                {this.state.segment_num > 0 &&
                                <button
                                    className={"btn btn-outline-dark mr-2"}
                                    onClick={() => this.prevSegment()}
                                >
                                    Back
                                </button>
                                }
                                {!(this.state.segment_num == doc.segments.length - 1
                                    && this.state.rereading)
                                    ? <button
                                        className={"btn btn-outline-dark"}
                                        onClick={() => this.nextSegment()}
                                    >
                                        {this.state.rereading ? 'Next' : 'Reread'}
                                    </button>
                                    : <button
                                        className={"btn btn-outline-dark"}
                                        onClick={() => this.toOverview()}
                                    > To Overview
                                    </button>
                                }
                            </div>
                            <div className={"col-4 input-group"}>
                                <input
                                    className={"form-control"}
                                    type="text"
                                    placeholder={"Page #"}
                                    onChange={this.handleJumpToFieldChange}
                                />
                                <button
                                    className={"btn btn-outline-dark form-control"}
                                    onClick={this.handleJumpToButton}
                                    //Checks isNaN so that an empty string doesn't count as 0
                                    disabled={Number.isNaN(this.state.jump_to_value) ||
                                        !this.state.segments_viewed.includes(
                                            this.state.jump_to_value)}
                                >
                                Jump
                                </button>
                            </div>
                        </div>
                    </React.Fragment>
                }
            </div>
        );

    }
}

export default ReadingView;
