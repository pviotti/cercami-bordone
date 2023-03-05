import React, { useState } from 'react';
import logo from './images/cb_logo.jpg';
import './App.css';

type GrepResult = {
    title: string;
    url: string;
    date: string;
    excerpts: string[];
}

function RenderResults({ data }: { data: GrepResult[] }) {
    const items = data.map(
        element => {
            return (
                <div className='box'>
                    <div className='content is-small'>
                        <>
                            <span className=''>{element.date} - <a href={element.url}>{element.title}</a></span>
                            <>
                                {element.excerpts.map(ex => {
                                    return (
                                        <blockquote className='blur-box'>
                                            ...{ex}...
                                        </blockquote>
                                    )
                                }
                                )}
                            </>
                        </>
                    </div>
                </div>
            )
        }
    )
    return <>{items}</>;
}


function App() {

    const [input, setInput] = useState("");
    const [results, setResults] = useState([]);

    const handleSearchClick = (_e: React.MouseEvent) => {
        if (input.length > 2) {
            fetch("http://localhost:5000/grep?q=" + input)
                .then((response) => response.json())
                .then((data) => {
                    setResults(data)
                    console.log(data)
                });
        }
    }

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const inputValue = e.target.value;
        if (inputValue !== "") {
            // setShowSuggestions(true);
        } else {
            setResults([]);
        }
        setInput(inputValue);
    }
    return (
        <>
            <section className="section is-small">
                <div className="columns is-centered">
                    <div className="column is-two-thirds">

                        <div className='section is-small columns is-centered image'>
                            <figure className="image">
                                <img src={logo} className="logo" alt="logo" />
                            </figure>
                        </div>

                        <div className="columns is-centered">
                            <div className="field has-addons">
                                <div className="control">
                                    <input className="input"
                                        type="text"
                                        placeholder="giappone"
                                        value={input}
                                        onChange={handleInputChange}
                                    />
                                </div>
                                <div className="control">
                                    <button className="button is-info" onClick={handleSearchClick}>
                                        Cerca
                                    </button>
                                </div>
                            </div>
                        </div>

                    </div>
                </div>
            </section>
            <section>
                <div className="columns is-centered">
                    <div className="column is-two-thirds">
                        <RenderResults data={results} />
                    </div>
                </div>
            </section>
            <footer className="footer">
                <div className="content has-text-centered is-small">
                    <p>
                        <b>Cercami Bordone</b> is a weekend project by <a href="https://github.com/pviotti">pviotti</a>.
                    </p>
                    <p>
                        Last episode transcribed: XYZ <br />
                        Total episodes in database: QWE <br />
                    </p>
                </div>
            </footer>
        </>
    );
}

export default App;
