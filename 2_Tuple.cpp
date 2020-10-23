
#include <iostream>
#include <random>
#include <thread>
#include <future>
#include <chrono> 

using namespace std;

vector <int> BruteForceMinMax(vector <vector <int>> grid, int n){
    thread::id this_id = this_thread::get_id();
    int min_max[n][2];
    int total_comparisons = 0;
    for(int i=n-1; i>=0; i--){
        cout << this_id << endl;
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

vector <vector <int>> getDiv(vector <vector <int>> grid, int x1, int x2, int y1, int y2){
    vector <vector <int>> return_div;
    for(int i=x1; i < x2; i++){
        vector <int> temp;
        for(int j=y1; j<y2; j++){
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
    auto start_br = chrono::high_resolution_clock::now();
    result = BruteForceMinMax(grid, n);
    auto stop_br = chrono::high_resolution_clock::now();
    auto duration_br = chrono::duration_cast<chrono::microseconds>(stop_br - start_br); 
    cout << "min : " << result[0] << endl;
    cout << "max : " << result[1] << endl;
    cout << "total_compares : " << result[2] << endl;
    cout << "brute force duration : " << duration_br.count() << endl;
    vector <vector <int>> div1 = getDiv(grid, 0, 50, 0, 50);
    vector <vector <int>> div2 = getDiv(grid, 50, 100, 0, 50);
    vector <vector <int>> div3 = getDiv(grid, 0, 50, 50, 100);
    vector <vector <int>> div4 = getDiv(grid, 50, 100, 50, 100);
    auto start_tr = chrono::high_resolution_clock::now();
    future <vector <int>> t1 = async(launch::async, BruteForceMinMax, div1, 50);  
    future <vector <int>> t2 = async(launch::async, BruteForceMinMax, div2, 50);  
    future <vector <int>> t3 = async(launch::async, BruteForceMinMax, div3, 50);  
    future <vector <int>> t4 = async(launch::async, BruteForceMinMax, div4, 50);  
    vector <int> d1 = t1.get();
    vector <int> d2 = t2.get();
    vector <int> d3 = t3.get();
    vector <int> d4 = t4.get();
    cout << d1[0] << " " << d1[1] << " " << d1[2] << endl;
    cout << d2[0] << " " << d2[1] << " " << d2[2] << endl;
    cout << d3[0] << " " << d3[1] << " " << d3[2] << endl;
    cout << d4[0] << " " << d4[1] << " " << d4[2] << endl;

    vector <vector <int>> thread_returns;
    thread_returns.push_back(d1);
    thread_returns.push_back(d2);
    thread_returns.push_back(d3);
    thread_returns.push_back(d4);

    int glob_min = thread_returns[0][0];
    int glob_max = thread_returns[0][1];
    int glob_compares = 0;

    for(auto ret : thread_returns){
        if(ret[0] < glob_min){
            glob_min = ret[0];
        }
        if(ret[1] > glob_max){
            glob_max = ret[1];
        }
        glob_compares += ret[2];
    }
    auto stop_tr = chrono::high_resolution_clock::now();
    auto duration_tr = chrono::duration_cast<chrono::microseconds>(stop_tr - start_tr); 
    cout << "global min : " << glob_min << endl;
    cout << "global max : " << glob_max << endl;
    cout << "global compares : " << glob_compares << endl;
    cout << "thread duration : " << duration_tr.count() << endl;
}