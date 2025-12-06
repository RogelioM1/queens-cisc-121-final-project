import gradio as gr
import plotly.graph_objects as go
import time

# ----------------- Chart functions -----------------
def create_segment_chart(left, right, i, j):
    arr = left + right
    colors = ["lightblue"] * len(left) + ["lightgreen"] * len(right)
    if 0 <= i < len(left):
        colors[i] = "red"
    if 0 <= j < len(right):
        colors[len(left) + j] = "orange"
    fig = go.Figure([go.Bar(x=list(range(len(arr))), y=arr, marker_color=colors)])
    fig.update_layout(
        yaxis=dict(range=[0, max(arr)+5] if arr else [0,1]),
        title="Left (blue) vs Right (green) sorted segments with pointers",
        height=300,
        margin=dict(l=20, r=20, t=20, b=20)
    )
    return fig

def create_merged_chart(arr, highlight=[], title="Merged Segment"):
    colors = ["lightgray"] * len(arr)
    for idx in range(len(arr)):
        if arr[idx] != 0:
            colors[idx] = "blue"
    for idx in highlight:
        if idx < len(arr):
            colors[idx] = "red"
    fig = go.Figure([go.Bar(x=list(range(len(arr))), y=arr, marker_color=colors)])
    fig.update_layout(
        yaxis=dict(range=[0, max(arr)+5] if arr else [0,1]),
        title=title,
        height=300,
        margin=dict(l=20, r=20, t=20, b=20)
    )
    return fig

def create_full_chart(full_arr, highlight=[], title="Full Array"):
    colors = ["blue"] * len(full_arr)
    for idx in highlight:
        if idx < len(full_arr):
            colors[idx] = "red"
    fig = go.Figure([go.Bar(x=list(range(len(full_arr))), y=full_arr, marker_color=colors)])
    fig.update_layout(
        yaxis=dict(range=[0, max(full_arr)+5] if full_arr else [0,1]),
        title=title,
        height=300,
        margin=dict(l=20, r=20, t=20, b=20)
    )
    return fig

# ----------------- Merge Sort Generator -----------------
def merge_sort_gen(arr, full_arr, offset=0, delay=0.2):
    n = len(arr)
    if n > 1:
        mid = n // 2
        left = arr[:mid]
        right = arr[mid:]

        for seg_chart, merged_chart, full_chart in merge_sort_gen(left, full_arr, offset, delay):
            yield seg_chart, merged_chart, full_chart
        for seg_chart, merged_chart, full_chart in merge_sort_gen(right, full_arr, offset + mid, delay):
            yield seg_chart, merged_chart, full_chart

        i = j = k = 0
        merged = [0] * n
        while i < len(left) and j < len(right):
            seg_chart = create_segment_chart(left, right, i, j)
            if left[i] < right[j]:
                merged[k] = left[i]
                full_arr[offset + k] = left[i]
                i += 1
            else:
                merged[k] = right[j]
                full_arr[offset + k] = right[j]
                j += 1
            merged_chart = create_merged_chart(merged.copy(), highlight=[k])
            full_chart = create_full_chart(full_arr.copy(), highlight=[offset+k], title=f"Full Array updating index {offset+k}")
            if delay > 0:
                time.sleep(delay)
            yield seg_chart, merged_chart, full_chart
            k += 1

        while i < len(left):
            seg_chart = create_segment_chart(left, right, i, j-1 if j>0 else -1)
            merged[k] = left[i]
            full_arr[offset + k] = left[i]
            i += 1
            merged_chart = create_merged_chart(merged.copy(), highlight=[k])
            full_chart = create_full_chart(full_arr.copy(), highlight=[offset+k], title=f"Full Array updating index {offset+k}")
            if delay > 0:
                time.sleep(delay)
            yield seg_chart, merged_chart, full_chart
            k += 1

        while j < len(right):
            seg_chart = create_segment_chart(left, right, i-1 if i>0 else -1, j)
            merged[k] = right[j]
            full_arr[offset + k] = right[j]
            j += 1
            merged_chart = create_merged_chart(merged.copy(), highlight=[k])
            full_chart = create_full_chart(full_arr.copy(), highlight=[offset+k], title=f"Full Array updating index {offset+k}")
            if delay > 0:
                time.sleep(delay)
            yield seg_chart, merged_chart, full_chart
            k += 1

        arr[:] = merged

    yield create_segment_chart(arr.copy(), [], -1, -1), create_merged_chart(arr.copy(), title="Segment sorted"), create_full_chart(full_arr.copy(), title="Full Array progress")

# ----------------- Gradio Functions -----------------
def sort_animation(user_input):
    try:
        arr = [int(x.strip()) for x in user_input.split(",")]
    except:
        empty_chart = create_segment_chart([], [], 0, 0)
        return empty_chart, empty_chart, empty_chart
    
    full_arr = arr.copy()
    for seg_chart, merged_chart, full_chart in merge_sort_gen(arr, full_arr, delay=0.2):
        yield seg_chart, merged_chart, full_chart

def sort_no_delay(user_input):
    try:
        arr = [int(x.strip()) for x in user_input.split(",")]
    except:
        empty_chart = create_segment_chart([], [], 0, 0)
        return empty_chart, empty_chart, empty_chart
    
    full_arr = arr.copy()
    for seg_chart, merged_chart, full_chart in merge_sort_gen(arr, full_arr, delay=0):
        yield seg_chart, merged_chart, full_chart

# ----------------- Gradio Interface -----------------
with gr.Blocks() as demo:
    # Top row: input box expands fully, buttons stacked right
    with gr.Row():
        # Input box column takes most of the space
        with gr.Column(scale=8):
            user_list = gr.Textbox(label="Enter numbers separated by commas", value="")
        # Buttons column with smaller scale
        with gr.Column(scale=2, min_width=130):
            btn_merge = gr.Button("Merge (slow)", variant="primary")
            btn_no_delay = gr.Button("Merge (fast)", variant="secondary")
        
    # Middle row: segment + merged charts side by side
    with gr.Row():
        chart_segment = gr.Plot(create_segment_chart([0]*3, [0]*3, 0, 0))
        chart_merged = gr.Plot(create_merged_chart([0]*6))
    
    # Bottom row: full array chart
    chart_full = gr.Plot(create_full_chart([]))
    
    # Connect buttons
    btn_merge.click(fn=sort_animation, inputs=user_list, outputs=[chart_segment, chart_merged, chart_full])
    btn_no_delay.click(fn=sort_no_delay, inputs=user_list, outputs=[chart_segment, chart_merged, chart_full])

demo.launch()
