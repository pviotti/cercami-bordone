import React from 'react';
import logo from './images/cb_logo.jpg';
import './App.css';

type GrepResult = {
    title: string;
    url: string;
    content: string;
}

function SearchResult({title, url, content}: GrepResult) {
    return (
        <div className='box'>
            <div className='content is-small'>
                <span className=''><a href={url}>{title}</a></span>
                <blockquote className='blur-box'>
                    ...{content}...
                </blockquote>
            </div>

        </div>
    );
}



function App() {
    return (
        <>
            <section className="section is-medium">
                <div className="columns is-centered">
                    <div className="column is-two-thirds">

                        <div className='section is-small columns is-centered image'>
                            <figure className="image">
                                <img src={logo} className="" alt="logo" />
                            </figure>
                        </div>

                        <div className="columns is-centered">
                            <div className="field has-addons">
                                <div className="control">
                                    <input className="input" type="text" placeholder="" />
                                </div>
                                <div className="control">
                                    <a className="button is-info">
                                        Cerca
                                    </a>
                                </div>
                            </div>
                        </div>

                    </div>
                </div>
            </section>
            <section>
                <div className="columns is-centered">
                    <div className="column is-two-thirds">
                        <SearchResult
                            title="Title of the episode"
                            url="https://duck.com"
                            content="Ut venenatis, nisl scelerisque sollicitudin fermentum, quam libero hendrerit ipsum,
                            ut blandit est tellus sit amet turpis"/>
                    </div>
                </div>
            </section>
        </>
    );
}

export default App;
