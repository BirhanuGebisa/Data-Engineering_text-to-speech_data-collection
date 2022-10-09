// frontend connection
import React, { useEffect } from 'react'
import { useState } from "react";
import { Recorder } from "react-voice-recorder";
import axios from 'axios';
const Home = () => {
    const [audioDetails, setAudioDetails] = useState({
        url: null,
        blob: null,
        chunks: null,
        duration: {
            h: 0,
            m: 0,
            s: 0
        }
    });
    const [text, setText] = useState({ "text": "" })
    const getText = async () => {
        let response = await axios.get("http://127.0.0.1:8000/loadText");
        let data = response.data;
        let textData = {
            "text": data["0"],
            "id": data["1"]
        }
        setText({ ...textData })
    }


    const handleAudioStop = (data) => {
        console.log(data);
        setAudioDetails({ ...data });
    };

    const handleAudioUpload = async (file) => {

        let base64data;
        var reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onloadend = async function () {
            base64data = reader.result;
            // console.log(base64data);

            let data = {
                "id": { ...text }.id,
                "base64": base64data
            }
            await axios.post(`http://127.0.0.1:8000/send`, data)
        }
        window.alert("Uploaded!")
    };

    const handleReset = () => {
        setAudioDetails({
            url: null,
            blob: null,
            chunks: null,
            duration: {
                h: 0,
                m: 0,
                s: 0
            }
        });
    };

    return (
        <div className="App">
            <div style={{ "width": "90vw", "marginInline": "auto", "padding": "5px", "textAlign": "left" }}>
                <h1>Text-to-Speech Data Collection System</h1>
            </div>
            <div style={{ "width": "90vw", "border": "1px solid black", "borderRadius": "10px", "marginInline": "auto", "padding": "5px", "height": "25px", "textAlign": "left", "marginBlock": "10px", "verticalAlign": "center" }}>
                {{ ...text }.text}
            </div>
            <div style={{ "width": "90vw", "marginInline": "auto", "padding": "5px", "textAlign": "left" }}>
                <button onClick={getText}
                    style={{ "padding": "10px" }}
                >
                    Get Text
                </button>
            </div>
            <div style={{ "width": "90vw", "marginInline": "auto", "padding": "5px", "textAlign": "left" }}>
                <Recorder
                    record={true}
                    // title={"Text to Speech Recording"}
                    audioURL={audioDetails.url}
                    showUIAudio
                    handleAudioStop={handleAudioStop}
                    handleAudioUpload={handleAudioUpload}
                    // handleCountDown={handleCountDown}
                    handleReset={handleReset}
                // mimeTypeToUseWhenRecording={`audio/webm`}
                />
            </div>
        </div>
    );
}

export default Home
