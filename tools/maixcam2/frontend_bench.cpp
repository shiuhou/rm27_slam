// Offline sparse-LK benchmark, no mapping or pose estimation.
#include <opencv2/opencv.hpp>
#include <opencv2/video/tracking.hpp>
#include <chrono>
#include <iostream>
#include <vector>
#include <algorithm>
#include <numeric>
#include <cstdio>
using Clock=std::chrono::steady_clock;
double ms(Clock::time_point t){return std::chrono::duration<double,std::milli>(Clock::now()-t).count();}
double percentile(std::vector<double> v,double q){if(v.empty())return 0;std::sort(v.begin(),v.end());return v[std::min(v.size()-1,(size_t)(q*(v.size()-1)))];}
int main(int argc,char**argv){
 if(argc!=6){std::cerr<<"raw_gray_file_or_stdin width frames max_points threads\n";return 2;}
 int width=std::stoi(argv[2]),limit=std::stoi(argv[3]),maxpts=std::stoi(argv[4]),threads=std::stoi(argv[5]);
 if((width!=336&&width!=672)||limit<1||maxpts<30||threads<1)return 2;
 int height=width==336?190:380;cv::setNumThreads(threads);
 FILE* input=std::string(argv[1])=="-"?stdin:fopen(argv[1],"rb");if(!input)return 3;
 cv::Mat raw,gray,old,small;std::vector<cv::Point2f> pts;
 std::vector<double> decode,processing,retention,active;int n=0;auto start=Clock::now();
 while(n<limit){
  auto tick=Clock::now();gray.create(height,width,CV_8U);if(fread(gray.data,1,width*height,input)!=(size_t)(width*height))break;decode.push_back(ms(tick));tick=Clock::now();
  if(!old.empty()&&!pts.empty()){
   std::vector<cv::Point2f> next,back,keep;std::vector<uchar>s,b;std::vector<float>e,be;
   cv::calcOpticalFlowPyrLK(old,gray,pts,next,s,e,cv::Size(15,15),2);
   cv::calcOpticalFlowPyrLK(gray,old,next,back,b,be,cv::Size(15,15),2);
   for(size_t j=0;j<pts.size();++j)if(s[j]&&b[j]&&e[j]<30&&cv::norm(pts[j]-back[j])<.75&&next[j].x>=8&&next[j].x<width-8&&next[j].y>=8&&next[j].y<height-8)keep.push_back(next[j]);
   retention.push_back((double)keep.size()/pts.size());pts.swap(keep);
  }
  if((int)pts.size()<maxpts*45/100||n%30==0){
   cv::Mat mask(gray.size(),CV_8U,cv::Scalar(255));mask.rowRange(0,8)=0;mask.rowRange(height-8,height)=0;mask.colRange(0,8)=0;mask.colRange(width-8,width)=0;
   for(auto&p:pts)cv::circle(mask,p,width==336?5:10,cv::Scalar(0),-1);
   if((int)pts.size()<maxpts){std::vector<cv::Point2f>extra;cv::goodFeaturesToTrack(gray,extra,maxpts-pts.size(),.015,width==336?5:10,mask,7);pts.insert(pts.end(),extra.begin(),extra.end());}
  }
  old=gray; // gray must be a distinct allocation on the next iteration
  gray.release();active.push_back(pts.size());processing.push_back(ms(tick));++n;
 }
 double elapsed=ms(start)/1000;double total=std::accumulate(processing.begin(),processing.end(),0.0);
 std::cout<<"{\"width\":"<<width<<",\"height\":"<<height<<",\"frames\":"<<n<<",\"max_points\":"<<maxpts<<",\"threads\":"<<threads<<",\"wall_seconds\":"<<elapsed<<",\"end_to_end_fps\":"<<n/elapsed<<",\"processing_fps_mean\":"<<n*1000/total<<",\"processing_ms_median\":"<<percentile(processing,.5)<<",\"processing_ms_p95\":"<<percentile(processing,.95)<<",\"decode_ms_median\":"<<percentile(decode,.5)<<",\"retention_median\":"<<percentile(retention,.5)<<",\"retention_p10\":"<<percentile(retention,.1)<<",\"retention_min\":"<<percentile(retention,0)<<",\"active_tracks_median\":"<<percentile(active,.5)<<"}\n";
 return n==limit?0:4;
}
