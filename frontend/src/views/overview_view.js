import React from "react";
import PropTypes from "prop-types";
import { Footer } from "../common";

class Navigation_Bar extends React.Component {
    render() {
        return (
            <nav className="navbar navbar-expand-md">
                <div className="navbar-nav row mr-4">
                    <a
                        className="navbar-title"
                        href="../../"
                    >
                        <h1>The<br/>Reading<br/>Redux</h1>
                    </a>
                </div>
                <div className="navbar-nav row">
                    <a
                        className="nav-link nav-item"
                        href="/project_overview/"
                    >Project Overview</a>
                    <a
                        className="nav-link nav-item"
                        href="/project_overview/sample/"
                    >Reading Sample</a>
                    <a
                        className="nav-link nav-item"
                        href="/project_overview/visuals/"
                    >Rereading Visuals</a>
                    <a
                        className="nav-link nav-item"
                        href="/project_overview/values/"
                    >Rereading Values</a>
                    <a
                        className="nav-link nav-item"
                        href="/project_overview/quantitative/"
                    >Quantitative Questions</a>
                    <a
                        className="nav-link nav-item"
                        href="/project_overview/sources/"
                    >Sources</a>
                    <a
                        className="nav-link nav-item"
                        href="/project_overview/writeups/"
                    >Student Reflections</a>
                </div>
            </nav>
        );
    }
}


export class OverviewContent extends React.Component {
    render() {
        return (
            <>
                <Navigation_Bar/>
                <main>
                    <div className="row">
                        <div className="col">
                            <h1 className="body-header"h1>{this.props.subtitle}</h1>
                            <div className="body-container">
                                {this.props.content}
                            </div>
                        </div>
                    </div>
                </main>
                <Footer />
            </>
        );
    }
}
OverviewContent.propTypes = {
    content: PropTypes.node,
    subtitle: PropTypes.string,
}


export class ReadingRedux extends React.Component {
    render() {
        const content = (
            <React.Fragment>
                <p className="body-text">
                    In literary studies we have a word to describe a novel that
                    traces the psychological and moral growth of its protagonist.
                    The word is <em>bildungsroman</em>. But I think it is at once
                    strange and unfortunate that we have no such word to describe a
                    category of research or writing that traces the development of a
                    real-life reader of a novel. This glaring lacuna might be a
                    consequence of the fact that we just do not have that kind of
                    data. That is, we do not know enough about if, how, or how much
                    a reader evolves via each encounter with a text. In a time when
                    it seems that bigots are getting bolder and louder all while
                    basically insisting that they are surfeited with learning new
                    things, which could actually help make them more tolerant (and
                    tolerable) people, it is perhaps consoling to remember that
                    human beings are in fact changeable. Reading is essential to
                    galvanizing those human changes. This Digital Humanities project
                    wants to affirm this claim by studying the effects of the
                    practice of <em>re-reading</em> a work of literature. The scope
                    of the project includes, but is not limited to, an attempt to
                    answer the following questions:
                </p>
                <ul>
                    <li>
                        <div className={"bullet-text"}>
                            If we can obtain data from a reader’s re-reading of a
                            text, then what might we learn about the intricacies of
                            the interrelated processes of reading, understanding,
                            and learning?
                        </div>
                    </li>
                    <li>
                        <div className={"bullet-text"}>
                            What can we discover about how exactly a reader is
                            reading differently upon rereading a text?
                        </div>
                    </li>
                    <li>
                        <div className={"bullet-text"}>
                            How many re-readings and over the course of how long a
                            period of time does it take to generate different
                            meanings of one text? Is there a way to direct or
                            expedite the process of readers making new meanings?
                        </div>
                    </li>
                    <li>
                        <div className={"bullet-text"}>
                            What are the various factors that motivate people to
                            reread texts in the first place?
                        </div>
                    </li>
                    <li>
                        <div className={"bullet-text"}>
                            What are the kinds of literary texts most conducive to
                            answering this project’s questions? In other words, what
                            are the texts that might be said to be especially
                            rereading-friendly?
                        </div>
                    </li>
                    <li>
                        <div className={"bullet-text"}>
                            We might very well know something about the
                            philosophical values of rereading, but what about its
                            numeric values, particularly in terms of the various
                            kinds of data it can generate as well as the
                            computational analysis we can use to interpret the data?
                        </div>
                    </li>
                    <li>
                        <div className={"bullet-text"}>
                            When a reader’s understanding of the meaning of a text
                            changes over time, how can we attribute this change to
                            how the reader has also changed over time—whether with
                            respect to age, mentality, political perspective,
                            gender, etc.?
                        </div>
                    </li>

                </ul>
                <p className="body-text">
                    While reproducibility and repeatability are expectations
                    required to verify the credibility of scientific experiments,
                    the kind of repetition with a difference that I hope to study
                    here underscores not only how different the Humanities is from
                    the Sciences but also how the Humanities <em>needs</em> to be
                    different from scientific protocols in order to make clear that
                    humanists value a changing human in an inevitably changing
                    world. We fully expect that repeated readings will produce
                    different responses and interpretations from readers. Indeed, we
                    want that quality of changeability for readers. I envision this
                    project being useful to students interested in learning how to
                    generate and appreciate the values of rereading; to instructors
                    who want and need to make the texts that they re-teach, year in
                    and year out, “come alive” not only for their students but also
                    for themselves; to cognitive psychologists curious about the
                    re-reading mind; to a general audience of readers eager to
                    understand both the qualitative and quantitative uses of our
                    encounters with literature.
                </p>
            </React.Fragment>
        );

        return (
            <OverviewContent
                content={content}
                subtitle="The Values of Rereading"
            />
        );
    }
}

export class RereadingSample extends React.Component {
    render() {
        const content = (
            <React.Fragment>
                <blockquote className="blockquote card card-body">
                    <p className="mb-0">
                        <q>The only short story I have ever
                            written, <q>Recitatif,</q> was
                            an experiment in the removal of all racial codes from a
                            narrative about two characters of different races for whom
                            racial identity is crucial.
                        </q>
                    </p>
                    <footer className="blockquote-footer">
                        Toni Morrison
                        <br/>
                        <strong>
                            Playing in the Dark: Whiteness and the Literary Imagination
                        </strong> (1992)
                    </footer>
                </blockquote>

                <blockquote className="blockquote card card-body">
                    <p className="mb-0">
                        <q>
                            In order to survive, you should re-read Toni [Morrison]
                            every ten years because every ten or fifteen years we have
                            to reimagine ourselves on this American landscape. You won’t
                            survive if you don’t do that.
                        </q>
                    </p>
                    <footer className="blockquote-footer">
                        Sonia Sanchez
                        <br/>
                        <strong>
                            Toni Morrison: The Pieces I Am
                        </strong> (2019)
                    </footer>
                </blockquote>
                <p className="body-text">
                    Since the form that most of Toni Morrison’s works of fiction take is
                    the novel, her only published short story, which never developed
                    into a full-blown novel, represents a special case. By the time of
                    “Recitatif”’s publication debut, Morrison had already published four
                    of what would eventually be eleven of her known novels. “Recitatif”
                    would have gone down in history as her only published short story
                    were it not for the publication, in February 2015, of “Sweetness,”
                    an excerpt of her then upcoming novel <em>God Help the Child</em>,
                    which was released in April 2015. So, since it wouldn’t be another
                    thirty-two years before she
                    wrote another “short story,” Morrison, more than anyone, seems
                    particularly aware of what a short story can do that a novel cannot.
                    Morrison, more than anyone, knows that she can wield a short story,
                    and
                    more importantly, she knows precisely how! In the case of
                    “Recitatif,”
                    it is safe to say that she understood that the form ideally suited
                    for
                    the re-readings that this narrative experiment tacitly prescribes
                    would
                    have to be something shorter than novel length; it would have to be
                    a
                    short story. A short story is conducive to re-readings.
                </p>

                <h4 className="body-subheader">
                    Why is “Recitatif” particularly appropriate for a
                    project about re-rereading?
                </h4>
                <ul>
                    <li>
                        <div className={"bullet-text"}>
                            After completing a first reading of the story, the
                            revelation about the narrative experiment encourages a
                            rereading; it encourages readers to do a double take, as it
                            were.
                        </div>
                    </li>
                    <li>
                        <div className={"bullet-text"}>
                            The short length and episodic structure—neatly demarcated by
                            five clearly different settings (or time frames)—facilitate
                            a rereading.
                        </div>
                    </li>
                    <li>
                        <div className={"bullet-text"}>
                            A story that effectively holds a mirror to our biases
                            provides the reader the opportunity to confront the workings
                            and retrace the trajectory of their reading self. The story
                            encourages readers to ask: How are the conclusions we jump
                            to about characters a direct reflection of how we read
                            them—i.e., of how we place them in a definite racial
                            category in this particular case? How do our biases obstruct
                            the quality and full potential of how we could read?
                        </div>
                    </li>
                    <li>
                        <div className={"bullet-text"}>
                            It is effectively a cautionary tale against speed reading
                            and making quick judgments.
                        </div>
                    </li>
                    <li>
                        <div className={"bullet-text"}>
                            Because “Sweetness” is not only a rival short story to some
                            extent, but also shares a similar theme with “Recitatif” (of
                            fraught mother-daughter relations), its existence as—more or
                            less—a foil to “Recitatif” also encourages a re-reading of
                            “Recitatif.” In other words, its very existence in her
                            oeuvre can’t help but compel us to ask the question: What,
                            if anything, does this new short story have to do with
                            Morrison’s <em>ur</em>-short story?
                        </div>
                    </li>
                    <li>
                        <div className={"bullet-text"}>
                            As narrative time passes, the story’s two main characters,
                            Roberta and Twyla—one of whom is the narrator—forget
                            important details about a third main character, Maggie, as
                            well as a childhood incident involving Maggie. Such memory
                            lapses suggest their unreliability as the tellers of
                            Maggie’s story and of the story of “Recitatif” itself, which
                            puts the onus on the reader to be a more careful reader than
                            they otherwise would have needed to be.
                        </div>
                    </li>
                </ul>
            </React.Fragment>
        );

        return (
            <OverviewContent
                content={content}
                subtitle="The Reading Sample: Recitatif"
            />
        );
    }
}

export class RereadingVisuals extends React.Component {
    render() {
        const content = (
            <React.Fragment>
                <h4 className="body-subheader">
                    How does one represent a reader’s multiple readings of one text?
                </h4>
                <h4 className="body-subheader">
                    How does one visualize a reader’s re-readings?
                </h4>
            </React.Fragment>
        );
        return (
            <OverviewContent
                content={content}
                subtitle="Rereading Visuals"
            />
        );
    }
}

export class RereadingValues extends React.Component {
    render() {
        const content = (
            <React.Fragment>
                <h4 className="body-subheader">
                    What are the numbers and statistics saying about rereading?
                </h4>
            </React.Fragment>
        );
        return (
            <OverviewContent
                content={content}
                subtitle="Rereading Values"
            />
        );
    }
}

export class QuantitativeQuestions extends React.Component {
    render() {
        const content = (
            <React.Fragment>
                <p>
                    Since this story is an intentionally calculated attempt at crafting
                    a very particular experience of reading, it prompts the question:
                    What is the recipe for this narrative experiment’s success? Or, what
                    exactly is the formula for this particular reading experience?
                </p>
                <p>So, here are some quantitative questions “Recitatif” raises:</p>
                <ol>
                    <li>
                        How many stereotypical assumptions about racial identity
                        constitute enough plausibility to keep the story going without
                        arousing suspicion in the reader about the story’s intentions?
                    </li>

                    <li>
                        What did Toni Morrison determine is the word-count threshold for
                        such a narrative experiment? (In other words, not only did
                        Morrison determine it had to be a short story but that it also
                        had to be a very specific length.)
                    </li>

                    <li>
                        How long can a writer sustain such a ruse? (In other words,
                        what is the final length of the short story Morrison decided on
                        after her own edits? *See Toni Morrison Papers.)
                    </li>

                    <li>
                        How does the story’s structure of five “acts” help distract the
                        reader from the story’s motives?
                    </li>
                    <li>
                        How is editing a form of linear optimization, and how can linear
                        optimization be applied to visualize Morrison’s editing process,
                        which has resulted in the final version of the narrative
                        structure and design of “Recitatif” available to readers since
                        its publication in 1983?
                    </li>

                    <li>
                        How do the story’s narrated time and narrative time
                        contribute to the story’s plausibility?

                        <br/>

                        <u>Narrated time</u>: period of time covered by the narrative;
                        the period of time during which the narrative is set.

                        <br/>

                        <u>Narrative time</u>: temporal structure of the narrative.
                    </li>
                </ol>
            </React.Fragment>
        );
        return (
            <OverviewContent
                content={content}
                subtitle="Quantitative Questions"
            />
        );
    }
}

export class Sources extends React.Component {
    render() {
        const content = (
            <React.Fragment>
                <ul>
                    <li>
                        <div className="bullet-text">
                            Gavin, Michael. “Vector Semantics, William Empson,
                            and the Study of Ambiguity,” <em>Critical Inquiry
                            44</em>,
                            Summer 2018.
                        </div>
                    </li>
                    <li>
                        <div className="bullet-text">
                            Morrison, Toni. <em>Playing in the Dark: Whiteness and
                            the Literary Imagination</em>. Cambridge, MA: Harvard
                            University Press, 1992. pp. xi.
                        </div>
                    </li>
                    <li>
                        <div className="bullet-text">
                            Morrison, Toni. “Recitatif.” <em>Confirmation: An
                            Anthology
                            of African American Women</em>, edited by Amiri Baraka
                            (LeRoi Jones) and Amina Baraka. New York: Quill, 1983.
                            pp. 243-261.
                        </div>
                    </li>
                    <li>
                        <div className="bullet-text">
                            Morrison, Toni. <em>Remember: The Journey to School
                            Integration</em>. New York: Houghton Mifflin Company,
                            2004.
                        </div>
                    </li>
                    <li>
                        <a
                            href="https://www.newyorker.com/magazine/ 2015/02/09/sweetness-2">
                            <div className="bullet-text">
                                Morrison, Toni. “Sweetness,”
                                <em>The New Yorker</em>,
                                February 2, 2015.
                            </div>
                        </a>
                    </li>
                    <li>
                        <div className="bullet-text">
                            Richard, I. A. “Introductory.” <em>Practical Criticism:
                            A Study of Literary Judgment</em>. San Diego, New York,
                            London: Harcourt Brace Jovanovich, 1962. pp. 3-16.
                        </div>
                    </li>

                    <li>
                        <div className="bullet-text">
                            Spacks, Patricia Meyer. <em>On Rereading</em>.
                            Cambridge, Mass.: Belknap Press of Harvard University
                            Press,
                            2011.
                        </div>
                    </li>
                    <li>
                        <div className="bullet-text">
                            <em>Toni Morrison: The Pieces I am</em>. Directed by
                            Timothy Greenfield-Sanders, Magnolia Pictures, 2019.
                        </div>
                    </li>
                </ul>
            </React.Fragment>
        );
        return (
            <OverviewContent
                content={content}
                subtitle="Sources"
            />
        );
    }
}


export class Writeups extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            writeups: null,
        };
    }

    async componentDidMount() {
        const url = '/api/writeups/';
        const response = await fetch(url, {
            headers: {
                'Content-type': 'application/json',
                'X-CSRFToken': this.csrftoken,
            }
        });
        const response_json = await response.json();
        this.setState({
            writeups: response_json
        });
    }

    render_one_writeup(writeup, i) {
        const create_markup = (tagged_text) => {
            return {
                __html: tagged_text
            };
        };

        return (
            <div key={i} className="card mb-4">
                <div className="card-header">
                    <h5>{writeup.title} {writeup.title !== '' && 'by'} {writeup.author}</h5>
                </div>
                <div className="card-body" dangerouslySetInnerHTML={create_markup(writeup.text)}/>
            </div>
        );
    }

    render() {
        const content = (
            <React.Fragment>
                {this.state.writeups &&
                    this.state.writeups.map(
                        (writeup, i) => this.render_one_writeup(writeup, i)
                    )
                }
            </React.Fragment>
        );
        return (
            <OverviewContent
                content={content}
                subtitle="Student Reflections"
            />
        );
    }
}

/*
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

 */
