import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import {FeedComponent, TweetsComponent, TweetDetailComponent} from './tweets'
import {ProfileBadgeComponent} from './profiles'
import * as serviceWorker from './serviceWorker';


const appEl = document.getElementById('root')
if (appEl) {
  ReactDOM.render(<App />, appEl);
}

const e = React.createElement

const tweetFeedEl = document.getElementById('tweetme-2-feed')
if (tweetFeedEl) {
  ReactDOM.render(
    e(FeedComponent, tweetFeedEl.dataset), 
    tweetFeedEl
  )
}

const tweetsEl = document.getElementById('tweetme-2')
if (tweetsEl) {
  ReactDOM.render(
    e(TweetsComponent, tweetsEl.dataset), 
    tweetsEl
  )
}

const tweetDetailEl = document.querySelectorAll(".tweetme-2-detail")
tweetDetailEl.forEach(container=> {
  ReactDOM.render(
    e(TweetDetailComponent, container.dataset), 
    container
  )
})

const userProfileBadgeEl = document.querySelectorAll(".tweetme-2-profile-badge")
userProfileBadgeEl.forEach(container=> {
  ReactDOM.render(
    e(ProfileBadgeComponent, container.dataset), 
    container
  )
})

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
