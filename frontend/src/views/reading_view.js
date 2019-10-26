import React from "react";
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
            show_analysis: false,
            document: null,
        }
    }

    async componentDidMount() {
        try {
            // Hardcode the document we know exists for now,
            // Generalize later...
            const response = await fetch('/api/documents/1');
            const document = await response.json();
            this.setState({document});
        } catch (e) {
            console.log(e);
        }

    }

    prevSegment () {
        // document will be replaced by actual data
        if (this.state.segmentNum > 0){
            this.setState({segmentNum: this.state.segmentNum-1});
        }
    }

    nextSegment () {
        // document will be replaced by actual data
        const length = this.state.document.segments.length;
        if (this.state.segmentNum < length){
            if (this.state.show_analysis === false) {
                this.setState({show_analysis: true});
            } else {
                this.setState({show_analysis: false, segmentNum: this.state.segmentNum+1});
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
                            <button onClick = {() => this.prevSegment()}>
                                Back
                            </button>
                            <button onClick = {() => this.nextSegment()}>
                                Next
                            </button>
                        </div>

                        { this.state.show_analysis &&
                            <div className={"analysis col-3"}>
                                <p><b>Prompts: </b>{prompts.map(el => "[" + el + "] ")}</p>
                                <p><b>Questions: </b>{questions.map(el => "[" + el.question + "] ")}</p>
                                <p><b>Add an annotation: </b><input
                                    type="text"
                                    value={this.state.value}
                                    onChange={this.handleChange}
                                /><button>Submit</button></p>
                            </div>
                        }
                    </div>
                </div>
                /* idea: maybe show the text again and allow highlighting and annotation (which
                   would show on mouse hover using popover
                 */
            );
        } else {
            return (
                <div>Loading!</div>
            );
        }
    }
}

export default ReadingView;
