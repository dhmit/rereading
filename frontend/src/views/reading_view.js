import React from "react";
import PropTypes from 'prop-types';

import {TimeIt} from "../common";
import './reading_view.css';


/*
 * Represents the actual Segment window
 */
class Segment extends React.Component {
    constructor(props) {
        super(props);
        this.segment_div_ref = React.createRef();
    }

    render() {
        const segment_lines = this.props.text.split("\r\n");
        return (
            <div
                className="segment my-3"
                ref={this.segment_div_ref}
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

    // We have the big arrow notation here to bind "this" to this function
    handleScroll = (e) => {
        const scroll_top = e.target.scrollTop;
        this.setState({scroll_top});
    };

    prevSegment () {
        this.updateData(false);
        this.setState({segment_num: this.state.segment_num-1});
        // this.segment_div_ref.current.scrollTo(0, 0);
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
        // this.segment_div_ref.current.scrollTo(0, 0);
    }

    recordScroll = () => {
        const scroll_data = this.state.scroll_data;
        scroll_data.push(this.state.scroll_top);
        this.setState({scroll_data});
    };

    async componentDidMount() {
        try {
            // Hard code the document we know exists for now,
            // Generalize later...
            const response = await fetch('/api/documents/1');
            const document = await response.json();
            const interval_timer = setInterval(this.recordScroll, 2000);
            this.setState({document, interval_timer });
            this.updateData(true);
        } catch (e) {
            console.log(e);
        }

    }

    render() {
        const doc = this.state.document;

        if (doc) {
            const current_segment = doc.segments[this.state.segment_num];
            const segment_text = current_segment.text;
            const segment_questions = current_segment.questions;
            const segment_contexts = current_segment.contexts;
            const document_questions = doc.document_questions;

            return (
                <div className={"container"}>
                    <h1 className={"display-4 py-3 pr-3"}>{doc.title}</h1>
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

                            <button
                                className={"btn btn-outline-dark"}
                                onClick={() => this.nextSegment()}
                            >
                                {this.state.rereading ? 'Next' : 'Reread'}
                            </button>
                        </div>

                        {this.state.rereading &&
                            <div className={"analysis col-4"}>
                                <p><b>Context: </b></p>
                                {segment_contexts.map((el,i) =>
                                    <ul key={i}>
                                        <li>{el.text}</li>
                                    </ul>)}
                                <p><b>Questions: </b></p>
                                {segment_questions.map((el,i) =>
                                    <ul key={i}>
                                        <li>{el.text}</li>
                                    </ul>
                                )}
                                {document_questions && (
                                    <p>
                                        <p><b>Document Questions: </b></p>
                                        {document_questions.map((el,i) =>
                                            <ul key={i}>
                                                <li>{el.text}</li>
                                            </ul>
                                        )}
                                    </p>
                                )}

                                <p>
                                    <b>Add an annotation: </b><input
                                        type="text"
                                        value={this.state.value}
                                        onChange={this.handleChange}
                                    /><button>Submit</button>
                                </p>
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
