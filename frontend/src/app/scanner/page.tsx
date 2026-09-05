"use client";
import React, { useState, useRef, useEffect } from 'react';
import Link from 'next/link';
import { useAuth } from "@/context/AuthContext";
import { useRouter } from "next/navigation";
import SidebarLayout from '@/components/SidebarLayout';
import AvatarMenu from '@/components/AvatarMenu';
import Breadcrumbs from '@/components/Breadcrumbs';

const getGrade = (score: number) => {
  if (score >= 90) return { letter: 'A', color: 'text-green-600', bg: 'bg-green-50', border: 'border-green-200', circle: 'border-green-500' };
  if (score >= 75) return { letter: 'B', color: 'text-green-500', bg: 'bg-green-50', border: 'border-green-200', circle: 'border-green-400' };
  if (score >= 60) return { letter: 'C', color: 'text-yellow-600', bg: 'bg-yellow-50', border: 'border-yellow-200', circle: 'border-yellow-500' };
  if (score >= 40) return { letter: 'D', color: 'text-orange-600', bg: 'bg-orange-50', border: 'border-orange-200', circle: 'border-orange-500' };
  return { letter: 'E', color: 'text-red-600', bg: 'bg-red-50', border: 'border-red-200', circle: 'border-red-500' };
};

const getFormulationTier = (score: number) => {
  if (score >= 80) return { label: 'Clean & Wholesome', color: 'text-brand', bg: 'bg-brand-light', fill: 'bg-brand' };
  if (score >= 40) return { label: 'Moderately Processed', color: 'text-yellow-700', bg: 'bg-yellow-50', fill: 'bg-yellow-500' };
  return { label: 'Highly Processed', color: 'text-red-700', bg: 'bg-red-50', fill: 'bg-red-500' };
};

export default function ScannerPage() {
  const { user, loading, getToken } = useAuth();
  const router = useRouter();

  const [file, setFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [step, setStep] = useState<1|2|3|4>(1); // 1: Capture, 2: Review, 3: Analyze, 4: Results
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [addingToBasket, setAddingToBasket] = useState(false);
  const [basketMsg, setBasketMsg] = useState("");

  const uploadInputRef = useRef<HTMLInputElement>(null);
  
  const [isCameraActive, setIsCameraActive] = useState(false);
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);

  const [progress, setProgress] = useState(0);
  const [progressText, setProgressText] = useState("Scanning image topology...");

  useEffect(() => {
    if (step === 3) {
      setProgress(0);
      setProgressText("Scanning image topology...");
      
      const texts = [
        { time: 0, text: "Scanning image topology..." },
        { time: 2000, text: "Extracting raw ingredients..." },
        { time: 4000, text: "Identifying hidden additives & INS codes..." },
        { time: 6000, text: "Cross-referencing TrueLabel database..." },
        { time: 8000, text: "Computing final nutritional profile..." }
      ];

      const timeouts = texts.map(t => 
        setTimeout(() => setProgressText(t.text), t.time)
      );

      const interval = setInterval(() => {
        setProgress(prev => Math.min(prev + 0.475, 95));
      }, 50);

      return () => {
        timeouts.forEach(clearTimeout);
        clearInterval(interval);
      };
    }
  }, [step]);

  useEffect(() => {
    if (!loading && !user) {
      router.push("/auth");
    }
  }, [user, loading, router]);

  useEffect(() => {
    return () => { stopCamera(); };
  }, []);

  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ 
        video: { facingMode: 'environment' } 
      });
      setIsCameraActive(true);
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
      }
    } catch (err) {
      console.error("Camera error:", err);
      alert("Could not access camera. Please check permissions or use the upload button.");
    }
  };

  const stopCamera = () => {
    if (videoRef.current && videoRef.current.srcObject) {
      const stream = videoRef.current.srcObject as MediaStream;
      stream.getTracks().forEach(track => track.stop());
      videoRef.current.srcObject = null;
    }
    setIsCameraActive(false);
  };

  const capturePhoto = () => {
    if (videoRef.current && canvasRef.current) {
      const video = videoRef.current;
      const canvas = canvasRef.current;
      
      const MAX_WIDTH = 1200;
      const MAX_HEIGHT = 1600;
      let width = video.videoWidth;
      let height = video.videoHeight;

      if (width > height) {
        if (width > MAX_WIDTH) {
          height *= MAX_WIDTH / width;
          width = MAX_WIDTH;
        }
      } else {
        if (height > MAX_HEIGHT) {
          width *= MAX_HEIGHT / height;
          height = MAX_HEIGHT;
        }
      }

      canvas.width = width;
      canvas.height = height;
      const ctx = canvas.getContext('2d');
      if (ctx) {
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        canvas.toBlob((blob) => {
          if (blob) {
            const capturedFile = new File([blob], "capture.jpg", { type: "image/jpeg" });
            setFile(capturedFile);
            setPreviewUrl(URL.createObjectURL(capturedFile));
            stopCamera();
            setStep(2);
          }
        }, 'image/jpeg', 0.7);
      }
    }
  };

  const compressImage = (file: File): Promise<File> => {
    return new Promise((resolve) => {
      const img = new Image();
      img.src = URL.createObjectURL(file);
      img.onload = () => {
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        const MAX_WIDTH = 1200;
        const MAX_HEIGHT = 1600;
        let width = img.width;
        let height = img.height;

        if (width > height) {
          if (width > MAX_WIDTH) {
            height *= MAX_WIDTH / width;
            width = MAX_WIDTH;
          }
        } else {
          if (height > MAX_HEIGHT) {
            width *= MAX_HEIGHT / height;
            height = MAX_HEIGHT;
          }
        }
        canvas.width = width;
        canvas.height = height;
        ctx?.drawImage(img, 0, 0, width, height);
        canvas.toBlob((blob) => {
            if(blob) {
                const newName = file.name.replace(/\.[^/.]+$/, "") + ".jpg";
                resolve(new File([blob], newName, { type: 'image/jpeg' }));
            } else {
                resolve(file); // fallback
            }
        }, 'image/jpeg', 0.7);
      };
      img.onerror = () => resolve(file); // fallback
    });
  };

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const selectedFile = e.target.files[0];
      const compressed = await compressImage(selectedFile);
      setFile(compressed);
      setPreviewUrl(URL.createObjectURL(compressed));
      stopCamera();
      setStep(2); // Move to review
    }
  };

  const handleRetake = () => {
    setFile(null);
    setPreviewUrl(null);
    setStep(1);
    setError(null);
  };

  const processImage = async () => {
    if (!file) return;
    setStep(3); // Analyzing
    setError(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const token = await getToken();
      const idToken = token || 'anonymous';

      // Step 1: ADK Orchestrator
      const response = await fetch('http://localhost:8003/api/v1/orchestrate/scanner', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${idToken}`
        },
        body: formData,
      });

      if (!response.ok) {
        if (response.status === 401) {
           throw new Error("Your session expired. Please refresh the page or log in again.");
        }
        let errBody = response.statusText;
        try {
          const errJson = await response.json();
          errBody = errJson.detail || JSON.stringify(errJson);
        } catch {
          errBody = await response.text() || response.statusText;
        }
        throw new Error(`Orchestration failed: ${errBody}`);
      }

      const data = await response.json();
      
      // Explicit AI Rejections (Blurry, Invalid Image, No Data)
      if (data.extracted_data?.error) {
        throw new Error(data.extracted_data.error_message || "Could not read the image.");
      }

      setResult(data);
      
      // Save to recent scans history (max 5)
      try {
        const historyStr = localStorage.getItem('recentScans');
        let history = historyStr ? JSON.parse(historyStr) : [];
        const newScan = {
          id: Date.now(),
          name: data.extracted_data?.name || "Unnamed Product",
          score: data.score?.nutritional_quality_score || 0,
          processing_score: data.score?.processing_score || 0,
          ingredients: data.extracted_data?.ingredients || [],
          timestamp: new Date().toISOString()
        };
        history.unshift(newScan);
        history = history.slice(0, 5); // Keep only last 5
        localStorage.setItem('recentScans', JSON.stringify(history));
      } catch (e) {
        console.error("Failed to save history", e);
      }
      
      setStep(4); // Results
    } catch (err: any) {
      console.error(err);
      setError(err.message || 'An error occurred during analysis.');
      setStep(2); // Back to review on error
    }
  };

  const handleAddToBasket = async () => {
    if (!user || !result?.extracted_data) return;
    setAddingToBasket(true);
    try {
      const token = await getToken();
      const payloadData = {
        ...result.extracted_data,
        score: result.score,
        biocontext: result.biocontext
      };
      
      const response = await fetch(`http://localhost:8007/api/v1/basket/add`, {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          product_data: payloadData
        }),
      });
      if (!response.ok) throw new Error('Failed to add');
      setBasketMsg('Added successfully!');
      setTimeout(() => setBasketMsg(''), 3000);
    } catch (err) {
      setBasketMsg('Failed to add');
    } finally {
      setAddingToBasket(false);
    }
  };

  if (loading || !user) return null;

  return (
    <SidebarLayout
      headerContent={
        <div className="flex items-center gap-2 sm:gap-4 text-[10px] sm:text-xs font-medium">
          <div className={`flex items-center gap-1 sm:gap-2 ${step >= 1 ? 'text-foreground' : 'text-gray-400'}`}>
            <span className={`w-4 h-4 sm:w-5 sm:h-5 rounded-full flex items-center justify-center text-[8px] sm:text-[10px] ${step >= 1 ? 'bg-brand text-white' : 'bg-gray-100'}`}>1</span>
            <span className="hidden sm:inline">Capture</span>
          </div>
          <div className="w-2 sm:w-8 h-px bg-gray-200"></div>
          <div className={`flex items-center gap-1 sm:gap-2 ${step >= 2 ? 'text-foreground' : 'text-gray-400'}`}>
            <span className={`w-4 h-4 sm:w-5 sm:h-5 rounded-full flex items-center justify-center text-[8px] sm:text-[10px] ${step >= 2 ? 'bg-brand text-white' : 'bg-gray-100'}`}>2</span>
            <span className="hidden sm:inline">Review</span>
          </div>
          <div className="w-2 sm:w-8 h-px bg-gray-200"></div>
          <div className={`flex items-center gap-1 sm:gap-2 ${step >= 3 ? 'text-foreground' : 'text-gray-400'}`}>
            <span className={`w-4 h-4 sm:w-5 sm:h-5 rounded-full flex items-center justify-center text-[8px] sm:text-[10px] ${step >= 3 ? 'bg-brand text-white' : 'bg-gray-100'}`}>3</span>
            <span className="hidden sm:inline">Analyze</span>
          </div>
          <div className="w-2 sm:w-8 h-px bg-gray-200"></div>
          <div className={`flex items-center gap-1 sm:gap-2 ${step >= 4 ? 'text-foreground' : 'text-gray-400'}`}>
            <span className={`w-4 h-4 sm:w-5 sm:h-5 rounded-full flex items-center justify-center text-[8px] sm:text-[10px] ${step >= 4 ? 'bg-brand text-white' : 'bg-gray-100'}`}>4</span>
            <span className="hidden sm:inline">Results</span>
          </div>
        </div>
      }
    >
      <div className="flex flex-col h-full w-full">
            
            {error && (
              <div className="mb-6 p-4 bg-red-50 text-red-600 border border-red-100 rounded-xl text-sm font-medium">
                {error}
              </div>
            )}

            {(step === 1 || step === 2) && (
              <div className="grid grid-cols-1 md:grid-cols-3 gap-12 h-full min-h-[500px]">
                {/* Left Text / Checklist */}
                <div className="flex flex-col justify-center space-y-8">
                  <div>
                    <h1 className="text-4xl font-serif text-brand mb-4">Scan any food product</h1>
                    <p className="text-sm text-gray-500 leading-relaxed">
                      Capture clear images of the front of the pack, ingredients list, and nutrition facts for complete intelligence.
                    </p>
                  </div>
                  <ul className="space-y-4">
                    {["Front of the pack", "Ingredients list", "Nutrition facts", "Claims (optional)"].map((item, i) => (
                      <li key={i} className="flex items-center gap-3 text-sm text-gray-600 font-medium">
                        <div className="w-5 h-5 rounded-full bg-brand-light flex items-center justify-center text-brand">
                          <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" /></svg>
                        </div>
                        {item}
                      </li>
                    ))}
                  </ul>
                </div>

                {/* Right Viewfinder */}
                <div className="md:col-span-2 bg-white rounded-3xl border border-gray-100 shadow-sm p-8 flex flex-col gap-8 items-center justify-center">
                   <input 
                     type="file" 
                     accept="image/*" 
                     ref={uploadInputRef}
                     onChange={handleFileChange}
                     className="hidden"
                   />
                   
                   <div className="flex flex-col gap-8 w-full items-center">
                     {/* Main Frame */}
                     <div 
                       className="relative w-full aspect-[3/4] max-w-sm rounded-2xl border-2 border-dashed border-gray-300 flex items-center justify-center bg-gray-50 overflow-hidden cursor-pointer hover:bg-gray-100 transition-colors"
                       onClick={isCameraActive ? capturePhoto : (step === 1 ? startCamera : undefined)}
                     >
                        <video ref={videoRef} autoPlay playsInline className={`w-full h-full object-cover ${isCameraActive ? 'block' : 'hidden'}`} />
                        <canvas ref={canvasRef} className="hidden" />
                        
                        {!isCameraActive && (
                          previewUrl ? (
                            <img src={previewUrl} alt="Preview" className="w-full h-full object-cover" />
                          ) : (
                            <div className="text-center">
                              <div className="w-16 h-16 rounded-full bg-white shadow-sm border border-gray-100 flex items-center justify-center mx-auto mb-4 text-gray-400">
                                <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" /></svg>
                              </div>
                              <p className="text-sm font-medium text-gray-500">Tap to activate camera</p>
                            </div>
                          )
                        )}
                        
                        {/* Corner markers */}
                        <div className="absolute top-4 left-4 w-6 h-6 border-t-2 border-l-2 border-brand"></div>
                        <div className="absolute top-4 right-4 w-6 h-6 border-t-2 border-r-2 border-brand"></div>
                        <div className="absolute bottom-4 left-4 w-6 h-6 border-b-2 border-l-2 border-brand"></div>
                        <div className="absolute bottom-4 right-4 w-6 h-6 border-b-2 border-r-2 border-brand"></div>
                     </div>

                     {/* Thumbnails Row */}
                     <div className="flex flex-row gap-6 justify-center">
                        {["Front", "Ingredients", "Nutrition"].map((label, i) => (
                          <div key={i} className="space-y-2 text-center">
                            <div className={`w-16 h-16 mx-auto rounded-xl border-2 ${i===0 && previewUrl ? 'border-brand' : 'border-gray-200 border-dashed'} bg-white overflow-hidden flex items-center justify-center text-[10px] text-gray-300 transition-colors`}>
                              {i===0 && previewUrl ? <img src={previewUrl} className="w-full h-full object-cover"/> : 'Empty'}
                            </div>
                            <span className="text-[11px] font-semibold text-gray-500">{label}</span>
                          </div>
                        ))}
                        <div className="space-y-2 text-center cursor-pointer">
                          <div className="w-16 h-16 mx-auto rounded-xl border border-gray-200 bg-gray-50 flex items-center justify-center text-gray-400 hover:bg-gray-100 transition-colors">
                            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" /></svg>
                          </div>
                          <span className="text-[11px] font-semibold text-gray-500">Add claims</span>
                        </div>
                     </div>
                   </div>

                   {/* Bottom Controls */}
                   <div className="flex justify-center items-center gap-12 mt-4 pt-4 border-t border-gray-100 w-full">
                     <button onClick={step === 1 ? (isCameraActive ? stopCamera : startCamera) : handleRetake} className="px-6 py-2 bg-white border border-gray-200 rounded-full text-xs font-bold text-gray-600 hover:bg-gray-50 transition-colors shadow-sm w-32">
                       {step === 1 ? (isCameraActive ? 'Cancel' : 'Open Camera') : 'Retake'}
                     </button>
                     
                     <div 
                        onClick={step === 1 ? (isCameraActive ? capturePhoto : startCamera) : processImage}
                        className="w-16 h-16 rounded-full border-4 border-gray-200 flex items-center justify-center cursor-pointer hover:border-brand transition-colors"
                      >
                       <div className={`w-12 h-12 rounded-full shadow-md ${isCameraActive ? 'bg-red-500' : 'bg-brand'}`}></div>
                     </div>
                     
                     <button onClick={step === 1 ? () => uploadInputRef.current?.click() : processImage} className="px-6 py-2 bg-white border border-gray-200 rounded-full text-xs font-bold text-gray-600 hover:bg-gray-50 transition-colors shadow-sm w-32">
                       {step === 1 ? 'Upload File' : 'Analyze'}
                     </button>
                   </div>
                </div>
              </div>
            )}

            {step === 3 && (
              <div className="flex-1 flex flex-col items-center justify-center max-w-md mx-auto w-full px-4 space-y-8 animate-fade-in">
                <div className="text-center space-y-2">
                  <h2 className="text-2xl font-serif text-brand">Analyzing Product</h2>
                  <p className="text-sm text-gray-500 h-6 transition-all">{progressText}</p>
                </div>
                
                <div className="w-full bg-gray-100 rounded-full h-3 overflow-hidden shadow-inner">
                  <div 
                    className="bg-brand h-full rounded-full transition-all duration-75 ease-out relative"
                    style={{ width: `${progress}%` }}
                  >
                    <div className="absolute inset-0 bg-white/20 w-full h-full"></div>
                  </div>
                </div>
                <div className="text-xs font-bold tracking-widest uppercase text-gray-400">
                  {Math.round(progress)}%
                </div>
              </div>
            )}

            {step === 4 && result && (
              <div className="space-y-8 animate-fade-in pb-12">
                 <div className="flex justify-between items-start">
                   <div>
                     <h1 className="text-3xl font-serif text-brand mb-1">{result.extracted_data?.name || 'Unnamed Product'}</h1>
                     <p className="text-sm text-gray-500">{result.extracted_data?.brand || 'Unknown Brand'} • {result.extracted_data?.category || 'Uncategorized'}</p>
                   </div>
                   <div className="flex flex-col items-end">
                     <button 
                       onClick={handleAddToBasket} 
                       disabled={addingToBasket}
                       className="px-6 py-2 bg-brand text-white rounded-lg text-sm font-medium hover:bg-brand-dark disabled:opacity-50 transition-colors"
                     >
                       {addingToBasket ? 'Adding...' : 'Add to Basket'}
                     </button>
                     {basketMsg && <span className="text-xs text-brand mt-2 font-medium">{basketMsg}</span>}
                   </div>
                 </div>

                 {/* Core Metrics Grid */}
                 <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    {/* Nutri-Score Widget */}
                    {result.score && (
                      <div className="bg-white p-6 rounded-3xl border border-gray-100 shadow-sm flex flex-col justify-between relative overflow-hidden group hover:shadow-md transition-shadow">
                        <div className="absolute -right-6 -top-6 w-24 h-24 bg-gray-50 rounded-full opacity-50 group-hover:scale-110 transition-transform"></div>
                        <h2 className="text-[10px] font-bold uppercase tracking-widest text-gray-400 mb-6 relative z-10">Nutritional Quality</h2>
                        
                        <div className="flex items-end justify-between relative z-10">
                          <div>
                            <div className={`w-14 h-14 rounded-2xl flex items-center justify-center text-2xl font-black text-white shadow-sm mb-3 ${getGrade(result.score.nutritional_quality_score).fill || 'bg-brand'}`}>
                              {getGrade(result.score.nutritional_quality_score).letter}
                            </div>
                            <p className="text-3xl font-serif text-foreground leading-none">{result.score.nutritional_quality_score}</p>
                            <p className="text-[10px] font-bold text-gray-400 uppercase tracking-wider mt-1">/ 100 Score</p>
                          </div>
                          
                          <div className="text-right">
                            <span className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold ${getGrade(result.score.nutritional_quality_score).bg} ${getGrade(result.score.nutritional_quality_score).color}`}>
                              Grade {getGrade(result.score.nutritional_quality_score).letter}
                            </span>
                          </div>
                        </div>
                      </div>
                    )}

                    {/* NOVA ML Widget */}
                    {result.score && (
                      <div className="bg-white p-6 rounded-3xl border border-gray-100 shadow-sm flex flex-col justify-between relative overflow-hidden group hover:shadow-md transition-shadow">
                        <div className="absolute -left-6 -bottom-6 w-32 h-32 bg-gray-50 rounded-full opacity-50 group-hover:scale-110 transition-transform"></div>
                        <h2 className="text-[10px] font-bold uppercase tracking-widest text-gray-400 mb-6 relative z-10 flex justify-between">
                          <span>Processing Level</span>
                          <span className="bg-brand text-white px-2 py-0.5 rounded text-[8px] tracking-widest">AI MODEL</span>
                        </h2>
                        
                        <div className="flex flex-col justify-end h-full relative z-10">
                           <p className="text-3xl font-serif text-foreground leading-none mb-2">{result.score.processing_score}</p>
                           
                           {/* Progress Bar */}
                           <div className="w-full h-1.5 bg-gray-100 rounded-full overflow-hidden mb-3">
                             <div className={`h-full rounded-full ${getFormulationTier(result.score.processing_score).fill}`} style={{ width: `${result.score.processing_score}%` }}></div>
                           </div>
                           
                           <div className="flex justify-between items-center">
                             <p className="text-[10px] font-bold text-gray-400 uppercase tracking-wider">Nourient AI</p>
                             <span className={`text-[10px] font-bold uppercase tracking-widest ${getFormulationTier(result.score.processing_score).color}`}>
                               {getFormulationTier(result.score.processing_score).label}
                             </span>
                           </div>
                        </div>
                      </div>
                    )}

                    {/* Metabolic Fit Widget */}
                    {result.biocontext ? (
                      <div className="bg-white p-6 rounded-3xl border border-gray-100 shadow-sm flex flex-col justify-between relative overflow-hidden group hover:shadow-md transition-shadow">
                        <div className="absolute right-0 top-0 w-full h-full bg-gradient-to-br from-white to-brand-light/30 opacity-50"></div>
                        <h2 className="text-[10px] font-bold uppercase tracking-widest text-gray-400 mb-4 relative z-10">Metabolic Fit</h2>
                        
                        <div className="relative z-10 flex flex-col h-full justify-between">
                          <div>
                            <div className="flex items-center gap-2 mb-2">
                              <span className="relative flex h-3 w-3">
                                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-brand opacity-40"></span>
                                <span className="relative inline-flex rounded-full h-3 w-3 bg-brand"></span>
                              </span>
                              <span className="text-xs font-bold text-brand uppercase tracking-widest">{result.biocontext.health_profile}</span>
                            </div>
                            <p className="text-3xl font-serif text-brand leading-none mb-1">{result.biocontext.metabolic_fit_score}</p>
                          </div>
                          
                          <p className="text-xs text-gray-500 leading-snug line-clamp-2" title={result.biocontext.context_reasoning}>
                            {result.biocontext.context_reasoning}
                          </p>
                        </div>
                      </div>
                    ) : (
                      <div className="bg-gray-50 p-6 rounded-3xl border border-dashed border-gray-200 flex flex-col items-center justify-center text-center">
                         <div className="w-10 h-10 rounded-full bg-gray-200 flex items-center justify-center mb-3 text-gray-400">
                           <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" /></svg>
                         </div>
                         <h3 className="text-xs font-bold text-gray-500 uppercase tracking-widest mb-1">Metabolic Fit</h3>
                         <p className="text-[10px] text-gray-400">Sign in to unlock personalized metabolic scoring.</p>
                      </div>
                    )}
                 </div>

                 {/* Recommendation Banner */}
                 {result.score && (
                   <div className={`p-4 rounded-2xl border flex items-center justify-between ${result.score.overall_recommendation.includes('LIMIT') ? 'bg-red-50 border-red-100' : 'bg-brand-light border-brand/20'}`}>
                     <div className="flex items-center gap-4">
                       <div className={`w-10 h-10 rounded-full flex items-center justify-center ${result.score.overall_recommendation.includes('LIMIT') ? 'bg-red-100 text-red-600' : 'bg-white text-brand'}`}>
                         <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                       </div>
                       <div>
                         <p className={`text-xs font-bold uppercase tracking-widest mb-1 ${result.score.overall_recommendation.includes('LIMIT') ? 'text-red-700' : 'text-brand'}`}>Nourient's Recommendation</p>
                         <p className={`text-lg font-serif leading-none ${result.score.overall_recommendation.includes('LIMIT') ? 'text-red-900' : 'text-brand-dark'}`}>{result.score.overall_recommendation}</p>
                       </div>
                     </div>
                     {/*<p className={`text-xs max-w-md hidden md:block ${result.score.overall_recommendation.includes('LIMIT') ? 'text-red-600/80' : 'text-brand-dark/80'}`}>
                       {result.score.reasoning}
                     </p>*/}
                   </div>
                 )}

                 <div className="grid grid-cols-1 gap-6">

                    {/* TrueLabel Auditor */}
                    {result.extracted_data?.audit && (
                      <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm h-full">
                        <h2 className="text-xs font-bold uppercase tracking-widest text-gray-400 mb-6">TrueLabel Auditor</h2>
                        <div className="space-y-4">
                          {result.extracted_data.audit.map((audit: any, idx: number) => (
                            <div key={idx} className={`p-4 rounded-xl border-l-4 ${audit.verdict === 'Deceptive' ? 'border-red-500 bg-red-50' : 'border-green-500 bg-brand-light'}`}>
                              <div className="flex justify-between items-start mb-2">
                                <span className="font-bold text-sm text-foreground">"{audit.claim}"</span>
                                <span className={`text-[10px] font-bold uppercase tracking-widest px-2 py-1 rounded-full ${audit.verdict === 'Deceptive' ? 'bg-red-100 text-red-700' : 'bg-green-100 text-brand'}`}>
                                  {audit.verdict}
                                </span>
                              </div>
                              <p className="text-xs text-gray-600">{audit.reasoning}</p>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                 </div>

                 {/* Ingredient Detective */}
                 {result.detective && (
                   <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm">
                     <h2 className="text-xs font-bold uppercase tracking-widest text-gray-400 mb-4 flex justify-between items-center">
                       Ingredient Detective
                       {(result.detective.flagged_ingredients?.length > 0 || result.detective.decoded_additives?.length > 0) && (
                         <span className="bg-red-50 text-red-600 px-2 py-1 rounded-full text-[10px]">Active</span>
                       )}
                     </h2>
                     <p className="text-sm text-gray-600 mb-6 leading-relaxed border-b border-gray-100 pb-6">
                       <span className="font-bold block mb-2 text-xs text-gray-400 uppercase tracking-widest">Raw Ingredient List</span>
                       {result.extracted_data?.ingredients?.map((ing: any) => 
                         ing.percentage ? `${ing.name} (${ing.percentage}%)` : ing.name
                       ).join(', ') || 'No ingredients detected.'}
                     </p>

                     {/* Deterministic Unified Decoder */}
                     {result.detective.decoded_additives?.length > 0 && (
                       <div className="mb-8">
                         <h3 className="font-bold text-xs text-foreground uppercase tracking-widest mb-3">Ingredients Decoded</h3>
                         <div className="space-y-2">
                           {result.detective.decoded_additives.map((additive: any, i: number) => (
                             <div key={i} className="flex flex-col md:flex-row md:items-center justify-between p-3 bg-white rounded-xl border border-gray-100 shadow-sm gap-4">
                               <div className="flex-1 min-w-0">
                                 <div className="flex items-center gap-2">
                                   <span className="font-bold text-sm text-foreground truncate">{additive.name}</span>
                                   {additive.code && <span className="text-[10px] text-gray-500 font-mono bg-gray-50 border border-gray-200 px-1.5 py-0.5 rounded shrink-0">{additive.code}</span>}
                                 </div>
                               </div>
                               <div className="flex flex-col sm:flex-row items-center gap-2 shrink-0">
                                 <span className="w-full sm:w-[130px] text-[9px] uppercase font-bold text-gray-500 tracking-widest bg-gray-50 border border-gray-100 px-2 py-1 rounded-full text-center shrink-0">{additive.source}</span>
                                 <span className="w-full sm:w-[150px] text-[9px] uppercase font-bold text-gray-500 tracking-widest bg-gray-50 border border-gray-100 px-2 py-1 rounded-full text-center shrink-0">{additive.category}</span>
                                 <span className={`w-full sm:w-[100px] text-[9px] uppercase font-bold tracking-widest px-2 py-1 rounded-full text-center shrink-0 ${
                                   additive.risk_level.toLowerCase() === 'safe' ? 'bg-green-100 text-green-700 border border-green-200' :
                                   additive.risk_level.toLowerCase() === 'moderate risk' || additive.risk_level.toLowerCase() === 'permitted additive' ? 'bg-yellow-100 text-yellow-700 border border-yellow-200' :
                                   additive.risk_level.toLowerCase() === 'unknown' ? 'bg-gray-100 text-gray-600 border border-gray-200' :
                                   'bg-red-100 text-red-700 border border-red-200'
                                 }`}>
                                   {additive.risk_level}
                                 </span>
                               </div>
                             </div>
                           ))}
                         </div>
                       </div>
                     )}

                     {/* AI Flagger */}
                     {result.detective.flagged_ingredients?.length > 0 && (
                       <div>
                         <h3 className="font-bold text-xs text-foreground uppercase tracking-widest mb-3">Flagged Concerns</h3>
                         <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                           {result.detective.flagged_ingredients.map((ing: any, i: number) => (
                             <div key={i} className="p-4 bg-red-50 rounded-xl border border-red-100">
                               <div className="flex justify-between items-center mb-2">
                                 <span className="font-bold text-sm text-red-700">{ing.name}</span>
                                 <span className="text-[10px] uppercase font-bold text-red-700 tracking-widest bg-red-100 px-2 py-1 rounded-full">{ing.purpose}</span>
                               </div>
                               <p className="text-xs text-red-600 mb-1">{ing.warning || ing.explanation}</p>
                               {ing.studies && <p className="text-[10px] text-red-400 italic mt-2 border-t border-red-100 pt-2">Studies: {ing.studies}</p>}
                             </div>
                           ))}
                         </div>
                       </div>
                     )}
                   </div>
                 )}
                 
                 <div className="flex justify-center mt-8">
                   <button onClick={handleRetake} className="px-6 py-2 border border-gray-200 bg-white rounded-lg text-sm font-medium text-gray-600 hover:bg-gray-50 transition-colors">
                     Scan Another Product
                   </button>
                 </div>
              </div>
            )}

      </div>
    </SidebarLayout>
  );
}
