# Daisy - A Hierarchical Friendly Federated Learning Framework For Edge Computing


## dev mode (virtual environment)
### 1. clone the source code
```
git clone https://github.com/Intelligent-Systems-Lab/daisy
```
### 2. build up environment
prepare and activate your virtual environment (python=3.8^)
```
cd daisy
./dev/bootstrap.sh
```
### develop<br>
### setup examples
don't overwrite daisyfl dependency in this step.<br>
```
cd <example_path>
pip install <pkgs_for_your_example>
```
### 5. run examples

## dev mode (docker)
### 1. clone the source code
```
git clone https://github.com/Intelligent-Systems-Lab/daisy
```
### 2. build up environment
```
docker run -it -v <daisy_source_code>:/root/daisy tcfwbper/daisyfl-dev:<version_tag> /bin/bash
```
### 3. develop<br>
### 4. setup examples<br>
don't overwrite daisyfl dependency in this step.<br>
```
docker attach <container_id>
```
```
cd <example_path> && conda activate daisy
pip install <pkgs_for_your_example>
```
### 5. run examples

## user mode
### 1. install daisyfl
```
pip install <daisyfl_version>
```
### 2. setup examples
```
pip install <pkgs_for_your_example>
```
### 3. run examples