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
Segment.propTypes = {
    text: PropTypes.string,
    handleScroll: PropTypes.func,
};


class OverviewWindow extends React.Component {
    render() {
        return (
            <div className={"row"}>
                <div className={"col-8"}>
                    <div className="scroll_overview">
                        {this.props.all_segments.map((el, i) => (
                            <p key={i}>{el.text}</p>)
                        )}
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
            segment_data: [],
            scroll_top: 0,
            scroll_data: [],
            rereading: false,  // we alternate reading and rereading
            document: null,
            interval_timer: null,
        }
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


    prevSegment () {
        this.updateData(false);
        this.setState({segment_num: this.state.segment_num-1});
        segment_ref.current.scrollTo(0,0);
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
        segment_ref.current.scrollTo(0,0);
    }

    recordScroll() {
        const scroll_data = this.state.scroll_data;
        scroll_data.push(this.state.scroll_top);
        //
        this.setState({scroll_data});
    }

    handleScroll(e) {
        const scroll_top = e.target.scrollTop;
        this.setState({scroll_top});
    }

    toOverview () {
        this.setState({overview: true})
    }

    async componentDidMount() {
        try {
            // Hard code the document we know exists for now,
            // Generalize later...
            const response = await fetch('/api/documents/1');
            const document = await response.json();
            const interval_timer = setInterval(() => this.recordScroll(), 2000);
            this.setState({document, interval_timer });
            this.updateData(true);
        } catch (e) {
            console.log(e);
        }

    }

    render() {
        const doc = this.state.document;

        if (doc) {
            const document_length = doc.segments.length;
            const current_segment = doc.segments[this.state.segment_num];
            const segment_text = current_segment.text;
            const segment_questions = current_segment.questions;
            const segment_contexts = current_segment.contexts;
            const all_segments = doc.segments;
            const document_questions = doc.questions;

            return (
                <div className={"container"}>
                    <h1 className={"display-4 py-3 pr-3"}>{doc.title}</h1>

                    {this.state.overview ?
                        <OverviewWindow
                            all_segments={all_segments}
                            document_questions={document_questions}
                        />
                        :
                        <div className={"row"}>
                            <div className={'col-8'}>
                                <p>Segment Number: {this.state.segment_num + 1}</p>
                                <Segment
                                    text={segment_text}
                                    handleScroll={(e) => this.handleScroll(e)}
                                />
                                {this.state.segment_num > 0 &&
                                <button
                                    className={"btn btn-outline-dark mr-2"}
                                    onClick={() => this.prevSegment()}
                                >
                                    Back
                                </button>
                                }
                                {this.state.segment_num < document_length - 1 ?
                                    <button
                                        className={"btn btn-outline-dark"}
                                        onClick={() => this.nextSegment()}
                                    >
                                        {this.state.rereading ? 'Next' : 'Reread'}
                                    </button> :
                                    <button
                                        className={"btn btn-outline-dark"}
                                        onClick={() => this.toOverview()}
                                    >
                                        To Overview
                                    </button>
                                }
                            </div>

                            {this.state.rereading &&
                                <div className={"analysis col-4"}>
                                    <p><b>Context: </b></p>
                                    {segment_contexts.map((el,i) =>
                                        <p key={i}>{el.text}</p>)}
                                    <p><b>Questions: </b></p>
                                    {segment_questions.map((el,i) =>
                                        <p key={i}>{el.text}</p>
                                    )}
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
                    }

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
