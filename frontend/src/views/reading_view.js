import React from "react";
// import PropTypes from 'prop-types';


class ReadingView extends React.Component {
    constructor(props){
        super(props);
        this.state = {
            segmentNum: 0,
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

    changeSegment (changeNum) {
        const newNum = this.state.segmentNum + changeNum;
        // document will be replaced by actual data
        if (newNum >= 0 && newNum < this.state.document.segments.length){
            this.setState({segmentNum: newNum});
        }
    }

    render() {
        // We're going to use this code for prompts, but right now
        // we're not actually getting them from the API!
        // <p><b>Prompts: </b>{data.prompts.map(el => "[" + el + "] ")}</p>
        const data = this.state.document;
        if (data) {
            return (
                <div className={"container"}>
                    <h1>{data.title}</h1>
                    <p>Segment Number: {this.state.segmentNum + 1}</p>
                    <p>{data.segments[this.state.segmentNum].text}</p>
                    <button onClick={() => this.changeSegment(-1)}>Back</button>
                    <button onClick={() => this.changeSegment(1)}>Next</button>
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
