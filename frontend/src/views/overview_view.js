import React from "react";
import './overview_view.css';
//import PropTypes from 'prop-types';

class Navigation_Bar extends React.Component {
    render() {
        return (
            <nav className={"navbar navbar-expand-md bg-light"}>
                <div className={"navbar-nav"}>
                    <a
                        className={"nav-link nav-item text-dark font-weight-bold"}
                        href={"#overview"}
                    >Project Overview</a>
                    <a
                        className={"nav-link nav-item text-dark font-weight-bold"}
                        href={"#sample"}
                    >The Reading Sample</a>
                    <a
                        className={"nav-link nav-item text-dark font-weight-bold"}
                        href={"#visuals"}
                    >Rereading Visuals</a>
                    <a
                        className={"nav-link nav-item text-dark font-weight-bold"}
                        href={"#values"}
                    >Rereading Values</a>
                    <a
                        className={"nav-link nav-item text-dark font-weight-bold"}
                        href={"#quantitative"}
                    >Quantitative Questions</a>
                </div>
            </nav>
        );
    }
}


export class ReadingRedux extends React.Component {
    render() {
        return (
            <div className="row"><div className="col">
                <a id="overview"><h1>The Reading Redux</h1></a>
                <h3>The Values of Rereading</h3>
                <p>
                    In literary studies we have a word to describe a novel that traces the
                    psychological and moral growth of its protagonist. The word is
                    <em> bildungsroman.</em> But I think it is at once strange and unfortunate that
                    we have no such word to describe a category of research or writing that traces
                    the development of a real-life reader of a novel. This glaring lacuna might be a
                    consequence of the fact that we just do not have that kind of data. That is, we
                    do not know enough about if, how, or how much a reader evolves via each
                    encounter with a text. In a time when it seems that bigots are getting bolder
                    and louder all while basically insisting that they are surfeited with learning
                    new things, which could actually help make them more tolerant (and tolerable)
                    people, it is perhaps consoling to remember that human beings are in fact
                    changeable. Reading is essential to
                    galvanizing those human changes. This Digital Humanities project wants to
                    affirm this claim by studying the effects of the practice of
                    <em> re-reading</em> a work
                    of literature. The scope of the project includes, but is not limited to, an
                    attempt to answer the following questions: If we can understand the outcomes of
                    re-reading a text, then what might we be able to deduce about how formative a
                    text really is and how people think differently, change their minds, or become
                    entirely different people as time goes by?
                </p>
                <ul>
                    <li>
                        What can we discover about how exactly a reader is reading
                        <em> differently</em> when we evaluate what that reader annotates
                        differently
                        upon rereading a text?
                    </li>
                    <li>
                        How many re-readings and over the course of how long a period of time does
                        it take to generate different meanings of one text? Is there a way to direct
                        or expedite that process of readers making new meanings?
                    </li>
                    <li>
                        What are the various factors that motivate people to reread texts in the
                        first place?
                    </li>
                    <li>
                        What kinds of literary texts are especially conducive to answering this
                        project’s questions?
                    </li>
                    <li>
                        When a reader’s understanding of the meaning of a text changes over time,
                        how can we attribute this change to how the reader has also changed over
                        time—whether with respect to age, mentality, political perspective, gender,
                        etc.?
                    </li>
                </ul>
                <p>
                    At least one positive consequence of this project I anticipate is that the
                    nagging question in literacy-education circles about how to help people
                    transform into better readers can become less about trying to get people to read
                    <em> more</em> and perhaps more about trying to get people to read, again and
                    again (and at different stages in their lives), some of the texts already in
                    their stock of
                    texts to read. Indeed, while reproducibility is a scientific aspiration required
                    to conduct scientific experiments, the kind of repetition with a difference that
                    I hope to study here underscores not only how different the Humanities is from
                    the Sciences but also how the Humanities <em> needs</em> to be different from
                    scientific
                    protocols in order to make clear that humanists value a changing human in an
                    inevitably changing world. I envision this project being useful to students
                    interested in learning how to appreciate the value of rereading books; to
                    instructors who want and need to make the texts that they re-teach, year in and
                    year out, “come alive” not only for their students but also for themselves; to
                    cognitive psychologists curious about the re-reading mind; to a general audience
                    of readers eager to understand both the qualitative and quantitative uses of
                    literature.
                </p>
            </div></div>
        );
    }
}

export class RereadingSample extends React.Component {
    render() {
        return(
            <div className="row"><div className="col">
                <a id="sample"><h1>The Reading Sample: Recitatif</h1></a>
                <h3>
                    <q>The only short story I have ever written, <q>Recitatif,</q> was an 
                    experiment in the removal of all racial codes from a narrative about two
                    characters of
                    different races for whom racial identity is crucial.</q>
                </h3>
                <p>
                    Since the form that most of Toni Morrison’s works of fiction take is the novel,
                    her only published short story, which never developed into a full-blown novel,
                    represents a special case. By the time of “Recitatif”’s publication debut,
                    Morrison had already published four of what would eventually be eleven of her
                    known novels. “Recitatif” would have gone down in history as her only published
                    short story were it not for the publication, in February 2015, of “Sweetness,”
                    an excerpt of her then upcoming novel God Help the Child, which was released in
                    April 2015. So, since it wouldn’t be another thirty-two years before she wrote
                    another “short story,” Morrison, more than anyone, seems particularly aware of
                    what a short story can do that a novel cannot. Morrison, more than anyone,
                    knows that she can wield a short story, and more importantly, she knows
                    precisely how! In the case of “Recitatif,” it is safe to say that she
                    understood that the form ideally suited for the re-readings that this narrative
                    experiment tacitly prescribes would have to be something shorter than novel
                    length; it would have to be a short story. A short story is conducive to
                    re-readings.
                </p>
                <h3>
                    Why is “Recitatif” particularly appropriate for a project about re-rereading?
                </h3>
                <ul>
                    <li>
                        After completing a first reading of the story, the revelation about the
                        narrative experiment encourages a rereading; it encourages readers to do a
                        double take, as it were.
                    </li>
                    <li>
                        The short length and episodic structure—neatly demarcated by five clearly
                        different settings (or time frames)—facilitate a rereading.
                    </li>
                    <li>
                        A story that effectively holds a mirror to our biases provides the reader
                        the opportunity to confront the workings and retrace the trajectory of
                        their reading self. The story encourages readers to ask: How are the
                        conclusions we jump to about characters a direct reflection of how we read
                        them—i.e., of how we placed them in a definite racial category?
                    </li>
                    <li>
                        It is effectively a cautionary tale against speed reading and making quick
                        judgments.
                    </li>
                    <li>
                        Because “Sweetness” is not only a rival short story to some extent, but
                        also shares a similar theme with “Recitatif” (of fraught mother-daughter
                        relations), its existence as—more or less—a foil to “Recitatif” also
                        encourages a re-reading of “Recitatif.” In other words, its very existence
                        in her oeuvre can’t help but compel us to ask the question: What, if
                        anything, does this new short story have to do with Morrison’s <em>ur</em>
                        -short story?
                    </li>
                    <li>
                        As narrative time passes, the story’s two main characters, Roberta and
                        Twyla—one of whom is the narrator—forget important details about a third
                        main character, Maggie, as well as a childhood incident involving Maggie.
                        Such memory lapses suggest their unreliability as the tellers of Maggie’s
                        story and of the story of “Recitatif” itself, which puts the onus on the
                        reader to be a more careful reader than they otherwise would have needed to
                        be.
                    </li>
                </ul>
            </div></div>
        );
    }
}

export class RereadingVisuals extends React.Component {
    render() {
        return(
            <div className="row">
                <div className="col">
                    <a id="visuals"><h1>Rereading Visuals</h1></a>
                    <h3>
                        How does one represent a reader’s multiple readings of one text?
                        How does one visualize a reader’s re-readings?
                    </h3>
                </div>
            </div>
        );
    }
}

export class RereadingValues extends React.Component {
    render() {
        return(
            <div className="row">
                <div className="col">
                    <a id="values"><h1>Rereading Values</h1></a>
                    <h3>What are the numbers and statistics saying about rereading?</h3>
                </div>
            </div>
        );
    }
}

export class QuantitiveQuestions extends React.Component {
    render() {
        return (
            <div className = "row">
                <div className="col">
                    <a id="quantitative"><h1>Quantitative Questions</h1></a>
                    <p>
                        Since this story is an intentionally calculated attempt at crafting a very
                        particular experience of reading, it prompts the question: What is the
                        recipe for this narrative experiment’s success? Or, what exactly is the
                        formula for this particular reading experience?
                    </p>
                    <p>So, here are some quantitative questions “Recitatif” raises:</p>
                    <ol>
                        <li>
                            How many stereotypical assumptions about racial identity constitute
                            enough plausibility to keep the story going without arousing
                            suspicion in the reader about the story’s intentions?
                        </li>

                        <li>
                            What did Toni Morrison determine is the word-count threshold for
                            such a narrative experiment? (In other words, not only did Morrison
                            determine it had to be a short story but that it also had to be a
                            very specific length.)
                        </li>

                        <li>
                            How long can a writer sustain such a ruse? (In other words, what is
                            the final length of the short story Morrison decided on after her
                            own edits? *See Toni Morrison Papers.)
                        </li>

                        <li>
                            How does the story’s structure of five “acts” help distract the
                            reader from the story’s motives?
                        </li>

                        <li>
                            How do the story’s narrated time and narrative time
                            contribute to the story’s plausibility?

                            <br />

                            <u>Narrated time</u>: period of time covered by the narrative;
                            the period of time during which the narrative is set.

                            <br />

                            <u>Narrative time</u>: temporal structure of the narrative.
                        </li>
                    </ol>
                </div>
            </div>
        )
    }
}

function render_participate_btn() {
    return (
        <div className="row mt-4"><div className="col text-center">
            <a
                className={"btn mx-auto btn-primary col-8"}
                href="/reading/"
            >Participate in our Study
            </a>
        </div></div>
    );
}

export class ProjectView extends React.Component {
    render() {
        return (
            <React.Fragment>
                <Navigation_Bar />
                <div className="container">
                    {render_participate_btn()}
                    <ReadingRedux />
                    <RereadingSample />
                    <RereadingVisuals />
                    <RereadingValues />
                    <QuantitiveQuestions />
                    {render_participate_btn()}
                </div>
            </React.Fragment>
        );
    }
}
