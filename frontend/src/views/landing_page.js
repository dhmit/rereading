import React from "react";
import { Footer } from "../common";
import {Modal, Button} from "react-bootstrap";

export class LandingPageView extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            show: true
        };
    }
    
    render() {
        const handleClose = () => this.setState({show: false});

        return (
            <>
                <Modal show={this.state.show} onHide={handleClose}>
                    <Modal.Header closeButton>
                        <Modal.Title>Archived Copy</Modal.Title>
                    </Modal.Header>
                    <Modal.Body>
                        The Reading Redux was a project by the <a href = "https://digitalhumanities.mit.edu/">
                        MIT Programs in Digital Humanities</a> in 
                        collaboration with our Fall 2019 Faculty Fellow, <a href = "https://lit.mit.edu/people/salexandre/">Sandy Alexandre</a>,
                        Associate Professor of Literature at MIT. The project 
                        has been archived, and is no longer being actively maintained.
                        <br/><br/>
                        The project contains student work, and there may be features which 
                        are incomplete or inaccurate.
                    </Modal.Body>
                    <Modal.Footer>
                        <Button variant="secondary" onClick={handleClose}>
                            Close
                        </Button>
                    </Modal.Footer>
                </Modal>
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


