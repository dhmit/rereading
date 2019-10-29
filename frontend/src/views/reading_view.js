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
            segmentNum: 0,
            timer: null,
            segmentReadTimes: [],
            segmentScrollUps: [],
            scrollTop: 0,
            scroll_ups: 0,
            scrolling_up: false,
            rereading: false,  // we alternate reading and rereading
            document: null,
        }
    }

    /**
     * segmentReadTimes is a array of arrays. The index of each array
     * corresponds to the segment number of the segments and is updated
     * with a new time every time the buttons are clicked
     */
    restartTimer(firstTime) {
        if (!firstTime) {
            const segmentReadTimes = this.state.segmentReadTimes;
            const time = this.state.timer.stop();
            segmentReadTimes[this.state.segmentNum].push(time);
            this.setState({segmentReadTimes,});
        }
        const timer = new TimeIt();
        this.setState({timer});
    }

    updateScrollUps() {
        const segmentScrollUps = this.state.segmentScrollUps;
        segmentScrollUps[this.state.segmentNum].push(this.state.scroll_ups);
        this.setState({segmentScrollUps, scroll_ups:0});
    }

    // We have the big arrow notation here to bind "this" to this function
    handleScroll = (e) => {
        this.setState(handleStoryScroll(e, this.state));
    };

    async componentDidMount() {
        try {
            // Hard code the document we know exists for now,
            // Generalize later...
            const response = await fetch('/api/documents/1');
            const document = await response.json();
            this.setState({document});
            this.restartTimer(true);
            let segmentReadTimes = this.state.segmentReadTimes;
            let segmentScrollUps = this.state.segmentScrollUps;
            for (let i = 0; i < document.segments.length; i++){
                segmentReadTimes.push([]);
                // Will need to make this account for the reread after merge
                segmentScrollUps.push([]);
            }
            this.setState({segmentReadTimes,});
            // This will allow the scroll detector to work
            window.addEventListener('scroll', this.handleScroll, true);
        } catch (e) {
            console.log(e);
        }

    }

    prevSegment () {
        // document will be replaced by actual data
        if (this.state.segmentNum > 0){
            this.restartTimer(false);
            this.updateScrollUps();
            this.setState({segmentNum: this.state.segmentNum-1});
        }
    }

    nextSegment () {
        const length = this.state.document.segments.length;
        if (this.state.segmentNum < length){
            if (this.state.rereading) {
                // If we're already rereading, move to the next segment
                this.restartTimer(false);
                this.updateScrollUps();
                this.setState({rereading: false, segmentNum: this.state.segmentNum+1});
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
            const segment = data.segments[this.state.segmentNum].text;

            return (
                <div className={"container"}>
                    <h1>{data.title}</h1>
                    <div className={"row"}>
                        <div className={"col-9"}>
                            <p>Segment Number: {this.state.segmentNum + 1}</p>
                            <p>{segment}</p>
                            {this.state.segmentNum > 0 &&
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
