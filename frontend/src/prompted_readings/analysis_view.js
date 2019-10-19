import React from "react";

class AnalysisView extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            // we initialize analysis to null, so we can check in render() whether
            // we've received a response from the server yet
            analysis: null,
        }
    }

    /**
     * This function is fired once this component has loaded into the DOM.
     * We send a request to the backend for the analysis data.
     */
    async componentDidMount() {
        try {
            const response = await fetch('/api/analysis/');
            const analysis = await response.json();
            this.setState({analysis});
        } catch (e) {
            // For now, just log errors to the console.
            console.log(e);
        }
    }

    render() {
        if (this.state.analysis !== null) {
            const {  // object destructuring:
                total_view_time,
            } = this.state.analysis;

            return (
                <div>
                    <h1>Analysis of Student Responses</h1>
                    <h3>Total view time</h3>
                    <p>{total_view_time} seconds</p>

                    <table>
                        <tr>
                            <th>{0}</th>
                            <th>{1}</th>
                            <th>{2}</th>
                            <th>{3}</th>
                        </tr>
                        <tr>
                            <td>{this.state.reread_counts.getKey("In one word," +
                                " how" +
                                " does this make you feel?").getKey("This is an" +
                                " ad.")}</td>
                            <td>{this.state.analysis.reread_counts().getKey("In one word, how" +
                                " does this make you feel?").getKey("This is an" +
                                "ad").getValue(0)}</td>
                            <td>{this.state.analysis.reread_counts().getKey("In one word, how" +
                                " does this make you feel?").getKey("This is an" +
                                "ad").getValue(1)}</td>
                            <td>{this.state.analysis.reread_counts().getKey("In one word, how" +
                                " does this make you feel?").getKey("This is an" +
                                "ad").getValue(2)}</td>
                            <td>{this.state.analysis.reread_counts().getKey("In one word, how" +
                                " does this make you feel?").getKey("This is an" +
                                "ad").getValue(3)}</td>
                        </tr>
                        <tr>
                            <td>{this.state.analysis.reread_counts().getKey("In one word, how" +
                                " does this make you feel?").getKey("This is a" +
                                " ashort story.")}</td>
                            <td>{this.state.analysis.reread_counts().getKey("In one word, how" +
                                " does this make you feel?").getKey("This is a short" +
                                "story.").getValue(0)}</td>
                            <td>{this.state.analysis.reread_counts().getKey("In one word, how" +
                                " does this make you feel?").getKey("This is a short" +
                                "story.").getValue(1)}</td>
                            <td>{this.state.analysis.reread_counts().getKey("In one word, how" +
                                " does this make you feel?").getKey("This is a short" +
                                "story.").getValue(2)}</td>
                            <td>{this.state.analysis.reread_counts().getKey("In one word, how" +
                                " does this make you feel?").getKey("This is a short" +
                                "story.").getValue(3)}</td>
                        </tr>
                    </table>
                </div>


            );
        } else {
            return (
                <div>Loading!</div>
            );
        }
    }


}

/*



*    renderTableHeader() {
      let header = Object.keys(this.state.students[0])
      return header.map((key, index) => {
         return <th key={index}>{key.toUpperCase()}</th>
      })
   }

   render() {
      return (
         <div>
            <h1 id='title'>React Dynamic Table</h1>
            <table id='students'>
               <tbody>
                  <tr>{this.renderTableHeader()}</tr>
                  {this.renderTableData()}
               </tbody>
            </table>
         </div>
      )
   }
*
* */


export default AnalysisView;
