# Merge Sort Visualization

## Hugging Face Link
[https://huggingface.co/spaces/rogeliom/CISC_121_Final_Project](https://huggingface.co/spaces/rogeliom/CISC_121_Final_Project)

## GitHub Link

[https://github.com/RogelioM1/queens-cisc-121-final-project](https://github.com/RogelioM1/queens-cisc-121-final-project)

## Steps to run program
The app has 6 elements. The first row of elements has a text box input where the user can input a comma-separated list to be sorted. Next to the input box are two buttons that will start the merge sort visualization, Merge (slow) will run through the merge process with a delay of 0.2 seconds, and the Merge (fast) will run through the merge process with no delay. 

In the second row, there are two bar charts. The first (on the left) shows the current left-hand segment and right-hand segment that it is merging. The different coloured bars represent the current value that the pointer is looking at. As the merging process happens and the pointers process both lists, the second chart (on the right) accumulates with the sorted values. 

In the last row, there is a single chart that represents the entire array as a whole. It shows where the second chart is being placed relative to the entire array. Since merge sort is an out-of-place sorting algorithm this chart makes the least sense, but I wanted to have a static visualization of where the list was being sorted instead of a bunch of unrelated charts being flashed across the screen. 

 

Upon inputting a list to be sorted the user will click the merge button and will see the segments being compared and understand how the pointers work to generate a sorted list. Since the small arrays of length 1 to ~4 flash by really fast it is hard to tell what is going on but by watching the last chart (full array) it is easy to understand where in the sorting process we are. The red pointer in the second chart lines up with the red pointer in the last chart to make sure that the user doesn’t get lost as merged segment constantly changes length.

## Computational Thinking Breakdown
Decomposition: 

Merge sort works by splitting the list in half and sorting both halves before merging them back together. The two halves implement merge sort again and it turns into a recursive loop of halving the list until all lists are a single item and then we can merge them back together in the right order. The two steps we need to focus on are the splitting and the merging. 

Pattern Recognition: 

The step that repeats is the merging of two individually sorted lists into a combined sorted list. Since both lists are sorted, we just compare the first items of both lists and add the smaller one iterating through until one list is empty and then add the rest to the back of the combined list. Once combined this merging step continues with the next two halves until the two halves you’re comparing are combined into the full original list. 

Abstraction: 

Since the splitting of the list is not very visual (the list is just being turned into to a list of lists), the process I’d want to show the user and see for myself is the merging part of the algorithm. 

Algorithm Design: 

The algorithm will get the user input via text box entry and then feed the input into a merge sort algorithm; the input will be parsed as a string of comma-separated values. We don’t need to visually show the list splitting in half but for the merging part I think if it were able to highlight the specific values for each pointer as it merges and then, if possible, have an animation of that value going into the combined list. Since there is no indication of the size of list the user will input, I think it could  be pretty cool to have the first ~3 recursions to show the block of code being executed and go slowly and then ramp up in speed as it goes along so that the animation time does not increase linearly with the length of the list.

## Flowchart

Flowchart is attached in GitHub

## Test Runs

Screenshots and video of a test run are attached in GitHub

## Author and Acknowledgements

No co-editors, chatgpt did most of the front-end and code cleaning. Prompts used below. 

Halfway through getting the front-end done, I decided to change the code to show three charts instead of just one. Since I was already lost in the code with all the gradio syntax I had chatgpt create the first two charts that only show the current segments with pointers and the merge of both segments. 

## Chatgpt prompts

“Can you create a gradio interface that has a textbox input and a bar chart output” 

“Is there a way to lock the input box from changing after clicking the button and unlock it via a function” didn’t end up using the code from this one 

“Is it possible to change the colour of one column in the bar chart” 

A lot of prompts something like “how to iteratively update the bar chart”, the bar chart kept returning an error or just not sorting the list or just not updating 

“Can you create an additional chart that represents the current segments being merged” 

“Can you create another chart that accumulates as the pointers iterate over both segments concurrently with the segment chart” 

Other prompts to get the front-end layout of the app, pasted my code with a prompt to try and get the right spacing of the app features 

## License

[MIT](https://choosealicense.com/licenses/mit/)
