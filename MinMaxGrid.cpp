#include <iostream>
#include <random>
#include <thread>
#include <future>

using namespace std;

vector <int> BruteForceMinMax(vector <vector <int>> grid, int n){
    int min_max[n][2];
    int total_comparisons = 0;
    for(int i=n-1; i>=0; i--){
        for(int j=0; j<n; j++){
            if(i==n-1){
                min_max[j][0] = grid[i][j];
                min_max[j][1] = grid[i][j];
            }
            else{
                if(grid[i][j] < min_max[j][0]){
                    min_max[j][0] = grid[i][j];
                }
                if(grid[i][j] > min_max[j][1]){
                    min_max[j][1] = grid[i][j];
                }                
                total_comparisons+=2;
            }
        }
    }
    int min, max;
    min = min_max[0][0];
    max = min_max[0][1];
    for(int i=0;i<n;i++){
        if(min_max[i][0] < min){
            min = min_max[i][0];
        }
        if(min_max[i][1] > max){
            max = min_max[i][1];
        }
        total_comparisons += 2;
    }
    vector <int> result = {min, max, total_comparisons};
    return result;
}

vector <vector <int>> getDiv(vector <vector <int>> grid, int lo, int hi){
    vector <vector <int>> return_div;
    for(int i=lo; i < hi; i++){
        vector <int> temp;
        for(int j=lo; j<hi; j++){
            temp.push_back(grid[i][j]);
        }
        return_div.push_back(temp);
    }
    return return_div;
}

int main(){
    int n;
    cout << "enter n" << endl;
    cin >> n;
    random_device rd;
    mt19937 gen(rd());
    uniform_int_distribution <> distr(0,1000);
    vector <vector <int>> grid;
    for(int i=0; i<n; i++){
        vector <int> temp;
        for(int j=0; j<n; j++){
            temp.push_back(distr(gen));
        }
        grid.push_back(temp);
    }
    vector <int> result;

    result = BruteForceMinMax(grid, n);
    cout << "min : " << result[0] << endl;
    cout << "max : " << result[1] << endl;
    cout << "total_compares : " << result[2] << endl;
}