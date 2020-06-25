import React from 'react'
import {apiTweetCreate} from './lookup'

export function TweetCreate(props){
    const textAreaRef = React.createRef()
    const {didTweet} = props
    const handleBackendUpdate = (response, status) => {
        if (status ===201) {
            didTweet(response)
        } else {
            alert('An error occured. Please try again!')
        }
    }
    const handleSubmit = (event) => {
        event.preventDefault()
        const newValue=textAreaRef.current.value
        // Backend api request
        apiTweetCreate(newValue,handleBackendUpdate)        
        textAreaRef.current.value = ''
    }
    return <div className={props.className}>
        <form onSubmit={handleSubmit}>        
            <textarea ref={textAreaRef} required={true} className='form-control' name = 'tweet'>
            </textarea>
            <button type='submit' className='btn btn-primary my-3'>Tweet</button>
        </form>
    </div>
}
