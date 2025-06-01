/* @refresh reload */
import { render } from 'solid-js/web'
import './index.module.sass'
import App from './App.tsx'

const root = document.getElementById('root')

render(() => <App />, root!)
