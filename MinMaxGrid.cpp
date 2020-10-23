#include <iostream>
#include <random>
#include <thread>
#include <future>
#include <chrono>

using namespace std;

int partition(int arr[], int l, int r)
{
    int x = arr[r], i = l;
    for (int j = l; j <= r - 1; j++)
    {
        if (arr[j] <= x)
        {
            swap(arr[i], arr[j]);
            i++;
        }
    }
    swap(arr[i], arr[r]);
    return i;
}

int kthSmallest(int arr[], int l, int r, int k)
{
    if (k > 0 && k <= r - l + 1)
    {

        int index = partition(arr, l, r);

        if (index - l == k - 1)
            return arr[index];

        if (index - l > k - 1)
            return kthSmallest(arr, l, index - 1, k);

        return kthSmallest(arr, index + 1, r,
                           k - index + l - 1);
    }
    return 0;
}

vector<int> BruteForceMinMax(vector<vector<int>> grid, int n, int n_tuples)
{
    int max[n][n_tuples / 2];
    int min[n][n_tuples / 2];
    int total_comparisons = 0;
    for(int j=0; j<n; j++){
        for (int m1 = 0; m1 < n_tuples / 2; m1++)
        {
            max[j][m1] = -1;
            min[j][m1] = 1000001;
        }

    }
    for (int i = n - 1; i >= 0; i--)
    {
        for (int j = 0; j < n; j++)
        {
            int temp1 = 0;
            int temp2 = 0;
            int temp_itr = 0;
            for (int m1 = 0; m1 < n_tuples / 2; m1++)
            {
                total_comparisons++;
                if(grid[i][j] == max[j][m1]){
                    cout << "wut" << endl;
                    break;
                }
                if (grid[i][j] > max[j][m1])
                {
                    temp1 = max[j][m1];
                    max[j][m1] = grid[i][j];
                    temp_itr = m1 + 1;
                    while (temp_itr < n_tuples / 2)
                    {
                        temp2 = max[j][temp_itr];
                        max[j][temp_itr] = temp1;
                        temp1 = temp2;
                        temp_itr++;
                    }
                    break;
                }
            }
            temp1 = 0;
            temp2 = 0;
            temp_itr = 0;
            for (int m1 = 0; m1 < n_tuples / 2; m1++)
            {
                total_comparisons++;
                if(grid[i][j] == max[j][m1]){
                    break;
                }
                if (grid[i][j] < min[j][m1])
                {
                    temp1 = min[j][m1];
                    min[j][m1] = grid[i][j];
                    temp_itr = m1 + 1;
                    while (temp_itr < n_tuples / 2)
                    {
                        temp2 = min[j][temp_itr];
                        min[j][temp_itr] = temp1;
                        temp1 = temp2;
                        temp_itr++;
                    }
                    break;
                }
            }
        }
    }

    int temp_result[n_tuples*n];
    vector<int> result;
    int ctr = 0;
    for(int i=0; i<n;i++){
        for(int j=0; j<n_tuples/2; j++){
            temp_result[ctr] = max[i][j];
            ctr++;
        }
        for(int j=0; j<n_tuples/2; j++){
            temp_result[ctr] = min[i][j];
            ctr++;
        }
    }
    for(int i=0; i<n_tuples/2; i++){
        int ret_value = kthSmallest(temp_result, 0, n_tuples*n - 1, i+1);
        result.push_back(ret_value);
        cout << ret_value << endl;
    }
    cout << endl;
    for(int i=0; i<n_tuples/2; i++){
        int ret_value = kthSmallest(temp_result, 0, n_tuples*n - 1, (n_tuples*n) - (i+1));
        result.push_back(ret_value);
        cout << ret_value << endl;
    }
    return result;
}

vector<vector<int>> getDiv(vector<vector<int>> grid, int x1, int x2, int y1, int y2)
{
    vector<vector<int>> return_div;
    for (int i = x1; i < x2; i++)
    {
        vector<int> temp;
        for (int j = y1; j < y2; j++)
        {
            temp.push_back(grid[i][j]);
        }
        return_div.push_back(temp);
    }
    return return_div;
}

int main()
{
    int n;
    cout << "enter n" << endl;
    cin >> n;
    random_device rd;
    mt19937 gen(rd());
    uniform_int_distribution<> distr(0, 1000000);
    vector<vector<int>> grid;
    for (int i = 0; i < n; i++)
    {
        vector<int> temp;
        for (int j = 0; j < n; j++)
        {
            temp.push_back(distr(gen));
        }
        grid.push_back(temp);
    }
    vector<int> result;
    auto start_br = chrono::high_resolution_clock::now();
    result = BruteForceMinMax(grid, n, 12);
    auto stop_br = chrono::high_resolution_clock::now();
    auto duration_br = chrono::duration_cast<chrono::microseconds>(stop_br - start_br);
    cout << "min : " << result[0] << endl;
    cout << "max : " << result[3] << endl;
    cout << "total_compares : " << result[2] << endl;
    cout << "brute force duration : " << duration_br.count() << endl;
/*
    vector<vector<int>> div1 = getDiv(grid, 0, 5000, 0, 5000);
    vector<vector<int>> div2 = getDiv(grid, 5000, 10000, 0, 5000);
    vector<vector<int>> div3 = getDiv(grid, 0, 5000, 5000, 10000);
    vector<vector<int>> div4 = getDiv(grid, 5000, 10000, 5000, 10000);
    auto start_tr = chrono::high_resolution_clock::now();
    future<vector<int>> t1 = async(launch::async, BruteForceMinMax, div1, 5000, 6);
    future<vector<int>> t2 = async(launch::async, BruteForceMinMax, div2, 5000, 6);
    future<vector<int>> t3 = async(launch::async, BruteForceMinMax, div3, 5000, 6);
    future<vector<int>> t4 = async(launch::async, BruteForceMinMax, div4, 5000, 6);
    vector<int> d1 = t1.get();
    vector<int> d2 = t2.get();
    vector<int> d3 = t3.get();
    vector<int> d4 = t4.get();
    cout << d1[0] << " " << d1[1] << " " << d1[2] << endl;
    cout << d2[0] << " " << d2[1] << " " << d2[2] << endl;
    cout << d3[0] << " " << d3[1] << " " << d3[2] << endl;
    cout << d4[0] << " " << d4[1] << " " << d4[2] << endl;

    vector<vector<int>> thread_returns;
    thread_returns.push_back(d1);
    thread_returns.push_back(d2);
    thread_returns.push_back(d3);
    thread_returns.push_back(d4);

    int glob_min = thread_returns[0][0];
    int glob_max = thread_returns[0][1];
    int glob_compares = 0;

    for (auto ret : thread_returns)
    {
        if (ret[0] < glob_min)
        {
            glob_min = ret[0];
        }
        if (ret[1] > glob_max)
        {
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
*/
}