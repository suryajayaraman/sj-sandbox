- The repo uses [Eigen library](https://eigen.tuxfamily.org/index.php?title=Main_Page) for matrix operations and [hungarian algorithm](../../fusion/hungarianAlgorithm/) implementation
- [Official python implementation](https://github.com/abewley/sort/blob/master/sort.py).

## Requirements
The code was developed on Ubuntu 20.04 LTS OS with
- g++ 9.4.0
- cmake 3.16.3
- Eigen 3.3
- OpenCV

## Reference Folder Structure
```
data/
    train/
        ADL-Rundle-6/
            det/det/txt
        ADL-Rundle-8/
            det/det.txt
        .....

mot_benchmark
    train/
        ADL-Rundle-6/
            det/det/txt
            gt/gt.txt
            img1/
                000001.jpg
                000002.jpg
                ......
```
- The `data/` folder contains necessary bounding box information for all frames in all scenarios
- The `mot_benchmark/` folder contains corresponding camera frames and is optional (~1.5GB download size)

## Results

### Python script runtime speed
![pyScriptRunTime](images/python_script_run_time_reference.png)
