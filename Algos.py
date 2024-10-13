def tower_of_hanoi(n, src, dest, aux):

    # Base case
    if n == 1:
        print(f"{n} {src} -> {dest}")

    # Recursive case
    else:
        tower_of_hanoi(n - 1, src, aux, dest)  # Move n-1 to aux

        # Move nth to dest
        print(f"{n} {src} -> {dest}")

        # Move n-1 from aux to dest
        tower_of_hanoi(n - 1, aux, dest, src)
