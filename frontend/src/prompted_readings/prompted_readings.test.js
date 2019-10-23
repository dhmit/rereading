import React from 'react';
import ReactDOM from 'react-dom';
import App from './student_view';
import {
  FrequencyFeelingTable, 
  ContextVsViewTime,
  SentimentScores,
} from "./analysis_view";

it('renders without crashing', () => {
    const div = document.createElement('div');
    ReactDOM.render(<App />, div);
    ReactDOM.unmountComponentAtNode(div);
});

it('FrequencyFeelingTable renders without crashing', () => {
    const div = document.createElement('div');
    const test_data = [
        ["happy", 30],
        ["surprised", 15],
    ];
    ReactDOM.render(<FrequencyFeelingTable feelings={test_data} />, div);
    ReactDOM.unmountComponentAtNode(div);
});

it('ContextVsViewTime renders without crashing', () => {
    const div = document.createElement('div');
    const test_data = {
        "This is a story": 2.873,
        "This is an ad": 3.987,
    };
    ReactDOM.render(<ContextVsViewTime viewTime={test_data}/>, div);
    ReactDOM.unmountComponentAtNode(div);
});

it('renders SentimentScores without crashing', () => {
    const div = document.createElement('div');
    ReactDOM.render(<SentimentScores />, div);
    ReactDOM.unmountComponentAtNode(div);
});