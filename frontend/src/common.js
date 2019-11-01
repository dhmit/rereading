/**
 * Common.js -- miscellaneous routines useful throughout the system
 */


import PropTypes from "prop-types";

/**
 * Get the value of a cookie, given its name
 * Adapted from https://docs.djangoproject.com/en/2.2/ref/csrf/#ajax
 * @param {string} name - The name of the cookie
 */
export function getCookie(name) {
    let cookieValue;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (const raw_cookie of cookies) {
            const cookie = raw_cookie.trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

/**
 * This is used as a helper function for keeping track of
 * how long a user has been looking at a story
 */
export class TimeIt {
    constructor() {
        this.start = Date.now();
        this.end = null;
        this.time = 0;
    }

    /**
     * This stops the timer and logs how long the timer has been running
     *
     * TODO: ensure that the timer has been running,
     * and that you are not calling stop() back to back
     */
    stop() {
        this.end = Date.now();
        this.time += this.end - this.start;
        return this.time / 1000;
    }

    /**
     * Restarts the timer while maintaining the current time that was stored,
     * useful for when someone takes a break or is no longer looking at the proper page
     */
    // noinspection JSUnusedGlobalSymbols
    resume() {
        this.start = Date.now();
    }
}

TimeIt.propTypes = {
    onScroll: PropTypes.func,
    onSubmit: PropTypes.func,
    onChange: PropTypes.func,
    answer: PropTypes.string,
    word_limit: PropTypes.number
};

/**
 * For large enough stories, this function logs how many times the user scrolls up to
 * read a previous portion of the story
 *
 * Note: This only tracks the number of times scrolled up, and not when the user scrolls
 * down to "advance" the story
 */
export function handleStoryScroll(e, scrollTop, scroll_ups, scrolling_up) {
    const current_scrollTop = e.target.scrollTop;
    const prev_scroll = scrollTop;
    // If the user is scrolling up, log it
    // console.log(current_scrollTop, prev_scroll);
    if (current_scrollTop < prev_scroll && !scrolling_up) {
        scroll_ups++;
        scrolling_up = true;
    } else if (current_scrollTop > prev_scroll && scrolling_up) {
        scrolling_up = false;
    }
    scrollTop = current_scrollTop;
    // For use with the setState function
    // console.log(scroll_ups);
    return {scrollTop, scroll_ups, scrolling_up};
}
