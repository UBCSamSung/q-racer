def game_loop(*args):
    if not game_started:
        frame = startFrame
    else:
        frame = baseFrame.copy()
        frame = place_dino(frame)
        frame = check_and_update_trees(frame)

        if not game_end:
            frame = place_tree(frame)
            new_score()
        else:
            print_score("Final")
            frame = endFrame

    im.set_data(frame)
    return im,

# RENDERER ===================================================

X_DIM = 50
Y_DIM = 15
RESOLUTION = 2
BASE_FRAME = np.ones((Y_DIM, X_DIM))

screen = plt.figure()

im = plt.imshow(BASE_FRAME, cmap='gray', vmin=0, vmax=1, animated=True)
ani = animation.FuncAnimation(screen, game_loop, frames=1000, interval=1, blit=False)

plt.xticks(np.arange(0, X_DIM, RESOLUTION))
plt.yticks(np.arange(0, Y_DIM, RESOLUTION))
plt.show()