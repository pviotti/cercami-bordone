import React, { useEffect, useState } from 'react';
import logo from './images/cb_logo.jpg';
import './App.css';

type GrepResult = {
    title: string;
    url: string;
    date: string;
    excerpts: string[];
}

type Stats = {
    last_episode_date: string;
    num_episodes: number;
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
    const [last_episode_date, setLastEpisodeDate] = useState("");
    const [num_episodes, setNumEpisodes] = useState(0);

    const handleSearchClick = (_e: React.MouseEvent) => {
        if (input.length > 2) {
            fetch("http://localhost:5000/grep?q=" + input)
                .then((response) => response.json())
                .then((data) => {
                    setResults(data)
                });
        }
    }

    useEffect(() => {
        fetch("http://localhost:5000/stats" + input)
            .then((response) => response.json())
            .then((data: Stats) => {
                setLastEpisodeDate(data.last_episode_date)
                setNumEpisodes(data.num_episodes)
            });
    }, []);

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
                                        Search
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
                        <b>Cercami Bordone</b> is a random project by <a href="https://github.com/pviotti">pviotti</a>.
                    </p>
                    <p>
                        Last episode transcribed: {last_episode_date}<br />
                        Number of episodes in database: {num_episodes}<br />
                    </p>
                </div>
            </footer>
        </>
    );
}

export default App;
