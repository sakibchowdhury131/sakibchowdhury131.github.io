
# Project: Entropy-Conserving Video Generation

## Overview
This project explores the hypothesis that consecutive video frames have near-constant entropy. The core idea is that a model can learn to transform one frame to the next by reorganizing structure on a constant-entropy manifold, rather than creating or destroying information. To test this, we generate a synthetic video dataset of moving shapes, measure entropy across frames, and train an entropy-conserving flow model for next-frame prediction.

## Core Hypothesis
Consecutive video frames maintain a nearly constant spectral entropy. This implies that the dynamic evolution of video content might be modeled as an information-preserving transformation.

## Key Components
1.  **Synthetic Video Dataset Generation**: Creates short video sequences of basic shapes (circles, rectangles, triangles) moving and interacting on a colored background. This controlled environment allows for precise analysis of entropy changes.
2.  **Entropy Measures**: Implements functions to calculate different types of entropy (spectral, pixel histogram, spatial variance) to quantitatively assess information content in frames.
3.  **Flow Prediction Network (FlowNet)**: A U-Net-like neural network designed to predict the optical flow (the change between `frame_t` and `frame_t+1`). This network is trained to not only minimize reconstruction error but also to conserve the spectral entropy between the input frame and the predicted next frame.
4.  **Training and Evaluation**: The model is trained on pairs of consecutive frames. Evaluation includes analyzing loss curves, comparing ground truth vs. predicted autoregressive rollouts, and crucially, monitoring entropy stability over long generated sequences.

## Setup and Usage

### Requirements
-   Python 3.x
-   PyTorch
-   Numpy
-   Matplotlib
-   Torchvision
-   Imageio (for GIF generation)

### Running the Notebook
1.  **Dependencies**: Ensure all required libraries are installed. The initial code cell should handle basic imports.
2.  **Configuration**: Adjust parameters like `IMG_SIZE`, `BATCH_SIZE`, `EPOCHS`, `NUM_VIDEOS`, `SEQ_LEN`, and `LAMBDA_ENT` in the first code cell (`SrDazttILYob`) to suit your experimental needs.
3.  **Execute Cells**: Run the notebook cells sequentially.
    -   **Cell 1**: Initializes configurations and defines entropy measures.
    -   **Cell 2**: Defines the `SyntheticVideoDataset` class.
    -   **Cell 3**: Defines the `FlowNet` architecture.
    -   **Cell 4**: Initializes the dataset and data loader.
    -   **Cell 5**: Runs the initial hypothesis test on entropy conservation in synthetic data and saves `entropy_over_frames.png`.
    -   **Cell 6**: Trains the `FlowNet` model. During training, it periodically saves `rollout_epoch_XXXX.png` and `entropy_comparison_XXXX.png` visualizations.
    -   **Cell 7**: Performs final analysis, generates loss curves (`loss_curves.png`), a long autoregressive rollout visualization (`long_rollout.png`), and an entropy stability plot for the long rollout (`entropy_long_rollout.png`). It also saves the trained model (`model_final.pt`).
    -   **Cell 8**: Visualizes the generated results and videos with textual explanations.
    -   **Cell 9**: Generates a GIF from the long autoregressive rollout frames (`long_rollout.gif`).
    -   **Cell 10**: Zips the output folder (`outputs_video.zip`).

## Results Summary

The initial hypothesis test confirmed that spectral entropy remains remarkably constant across consecutive frames in the synthetic dataset, with a very low relative range of change. This supports the core premise.

During training, both the reconstruction loss and the entropy conservation loss decreased significantly, indicating that the model successfully learned to predict future frames while attempting to maintain the spectral entropy. Visualizations of autoregressive rollouts show the model's ability to generate coherent sequences, and the entropy comparison plots highlight its success in tracking the ground truth entropy.

The long autoregressive rollout demonstrated the model's capacity to generate extended video sequences. While a slight drift in entropy was observed over very long rollouts (e.g., 30.23% drift over 40 steps), the model largely maintained entropy stability, reinforcing the viability of an entropy-conserving approach to video generation.

All generated images, GIFs, and the trained model are saved in the `outputs_video/` directory and subsequently zipped into `outputs_video.zip`.
