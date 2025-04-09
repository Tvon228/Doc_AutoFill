import { createSignal } from "solid-js"

export const useDropdownAnimation = () => {
	const [isAnimating, setIsAnimating] = createSignal(false)

	const startAnimation = (callback: () => void) => {
		if (isAnimating()) return
		setIsAnimating(true)
		callback()
		setTimeout(() => setIsAnimating(false), 100)
	}

	return { isAnimating, startAnimation }
}
