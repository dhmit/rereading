import React from "react";
import { Footer } from "../common";


export class LandingPageView extends React.Component {
    render() {
        return (
            <>
                <main className="text-center">
                    <h5 className='body-text'><em>
                        <a
                            href="https://lit.mit.edu/people/salexandre/"
                            className="landing-top-link"
                        >
                            Professor Sandy Alexandre
                        </a> and the
                        <a
                            href="https://digitalhumanities.mit.edu"
                            className="landing-top-link"
                        > MIT Programs in Digital Humanities
                        </a> present
                    </em></h5>
                    <h1 id="landing-header">The Reading Redux</h1>
                    <img
                        src="static/streshinsky_ted-girls_eating_lunch_at_school.jpg"
                        className="img-fluid"
                    />
                    <div className="row">
                        <div className="col">
                            <button
                                className="btn landing-btn col col-md-6"
                                onClick={() =>  window.location.href='/project_overview'}
                            >
                                Project Overview
                            </button>
                            <button
                                className="btn landing-btn col col-md-6"
                                onClick={() =>  window.location.href='/reading'}
                            >
                                Participate
                            </button>
                        </div>
                    </div>
                </main>
                <Footer />
            </>
        )
    }
}


