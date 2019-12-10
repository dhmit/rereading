import React from "react";

export class LandingPageView extends React.Component {
    render() {
        return (
            <div>
                <div className={"input-group-append"}>
                    <button
                        className={"btn start-btn "}
                        onClick={() =>  window.location.href='/project_overview'}
                    >
                        Project Overview
                    </button>
                </div>
                <div className={"input-group-append"}>
                    <button
                        className={"btn start-btn "}
                        onClick={() =>  window.location.href='/reading'}
                    >
                        Start Experiment
                    </button>
                </div>
            </div>
        )
    }
}
