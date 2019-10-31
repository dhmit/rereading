import React from "react";
import {TimeIt, handleStoryScroll} from "../common";
// import PropTypes from 'prop-types';

// THIS IS JUST FOR PROTOTYPING
// DELETE ME as soon as these data are included in the API endpoint
const PROMPTS_PROTOTYPE = ["this is an ad"];
const QUESTIONS_PROTOTYPE = [
    {
        question: "question_test",
        is_free_response: true,
        choices: [],
    },
    {
        question: "question_test2",
        is_free_response: false,
        choices: ["yes", "no"],
    },
];

class ReadingView extends React.Component {
    constructor(props){
        super(props);
        this.state = {
            segment_num: 0,
            timer: null,
            segment_read_times: [],
            segment_scroll_ups: [],
            scrollTop: 0,
            scroll_ups: 0,
            scrolling_up: false,
            rereading: false,  // we alternate reading and rereading
            document: null,
        }
    }

    /**
     * segment_read_times is a array of arrays. The index of each array
     * corresponds to the segment number of the segments and is updated
     * with a new time every time the buttons are clicked
     */
    restartTimer(firstTime) {
        if (!firstTime) {
            const segment_read_times = this.state.segment_read_times;
            const time = this.state.timer.stop();
            segment_read_times.push({
                read_time: time,
                is_rereading: this.state.rereading,
                segment_num: this.state.segment_num
            });
            this.setState({segment_read_times,});
        }
        const timer = new TimeIt();
        this.setState({timer});
    }

    updateScrollUps() {
        const segment_scroll_ups = this.state.segment_scroll_ups;
        segment_scroll_ups.push({
            scroll_ups: this.state.scroll_ups,
            is_rereading: this.state.rereading,
            segment_num: this.state.segment_num,
        });
        this.setState({segment_scroll_ups, scroll_ups:0});
    }

    // We have the big arrow notation here to bind "this" to this function
    handleScroll = (e) => {
        this.setState(handleStoryScroll(e, this.state.scrollTop, this.state.scroll_ups,
            this.state.scrolling_up));
    };

    async componentDidMount() {
        try {
            // Hard code the document we know exists for now,
            // Generalize later...
            const response = await fetch('/api/documents/1');
            const document = await response.json();
            this.setState({document});
            this.restartTimer(true);
            // This will allow the scroll detector to work
            window.addEventListener('scroll', this.handleScroll, true);
        } catch (e) {
            console.log(e);
        }

    }

    prevSegment () {
        // document will be replaced by actual data
        if (this.state.segment_num > 0){
            this.restartTimer(false);
            this.updateScrollUps();
            this.setState({segment_num: this.state.segment_num-1});
        }
    }

    nextSegment () {
        const length = this.state.document.segments.length;
        if (this.state.segment_num < length){
            if (this.state.rereading) {
                // If we're already rereading, move to the next segment
                this.restartTimer(false);
                this.updateScrollUps();
                this.setState({rereading: false, segment_num: this.state.segment_num+1});
            } else {
                // Otherwise, move on to the rereading layout
                this.restartTimer(false);
                this.updateScrollUps();
                this.setState({rereading: true});
            }
        }
    }


    render() {
        const data = this.state.document;

        if (data) {
            const questions = QUESTIONS_PROTOTYPE; // replace me with this.state.document.whatever
            const prompts = PROMPTS_PROTOTYPE; // replace me with this.state.document.whatever
            const segment = data.segments[this.state.segment_num].text;

            return (
                <div className={"container"}>
                    <h1>{data.title}</h1>
                    <div className={"row"}>
                        <div className={"col-9"}>
                            <p>Segment Number: {this.state.segment_num + 1}</p>
                            <p style={{fontSize: "50px"}}>{segment}</p>
                            {this.state.segment_num > 0 &&
                            <button onClick={() => this.prevSegment()}>
                                Back
                            </button>
                            }
                            <button onClick = {() => this.nextSegment()}>
                                {this.state.rereading ? 'Next' : 'Reread'}
                            </button>
                        </div>

                        {this.state.rereading &&
                            <div className={"analysis col-3"}>
                                <p><b>Prompts: </b>{prompts.map(el => "[" + el + "] ")}</p>
                                <p><b>Questions: </b>
                                    {questions.map(el => "[" + el.question + "] ")}
                                </p>
                                <p><b>Add an annotation: </b><input
                                    type="text"
                                    value={this.state.value}
                                    onChange={this.handleChange}
                                /><button>Submit</button></p>
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
