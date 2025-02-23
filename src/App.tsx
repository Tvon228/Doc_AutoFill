import classes from "./App.module.sass"
import MyDocs from "./components/features/MyDocuments"
import Header from "./components/layout/header"

function App() {
	return (
		<>
			<div class={classes.header}>
				<Header />
			</div>
			<div class={classes.content}>
				<div class={classes.main}>
					<MyDocs />
					<MyDocs />
					<MyDocs />
				</div>
			</div>
		</>
	)
}

export default App
