import React from "react";
// import PropTypes from 'prop-types';


class ReadingView extends React.Component {
    constructor(props){
        super(props);
        this.state = {
            segmentNum: 0,
            showing: false,
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
        if (this.state.showing === true) {
            this.setState({showing: !this.state.showing});
        }
    }

    // addAnnotation (startIndex, endIndex) {
    //
    // }

    render() {
        const data = this.state.document;

        if (data) {
            const questions = data.segments[this.state.segmentNum].questions;
            const segment = data.segments[this.state.segmentNum].text;

            return (
                <div className={"container"}>
                    <h1>{data.title}</h1>
                    <p>Segment Number: {this.state.segmentNum + 1}</p>
                    <p>{segment}</p>
                    <button onClick = {() => this.changeSegment(-1)}>Back</button>
                    <button onClick = {() => this.changeSegment(1)}>Next</button>
                    <button onClick = {() => this.setState({ showing: !this.state.showing })}>
                        Toggle analysis view</button>


                    { this.state.showing &&
                        <div className={"analysis"}>
                            <p><b>Prompts: </b>{data.prompts.map(el => "[" + el + "] ")}</p>
                            <p><b>Questions: </b>{questions.map(el => "[" + el.question + "] ")}</p>
                            <p>{segment}</p>
                            <p><b>Add an annotation: </b><input
                                type="text"
                                value={this.state.value}
                                onChange={this.handleChange}
                            /><button>Submit</button></p>
                        </div>
                    }
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
