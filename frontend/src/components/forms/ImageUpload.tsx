import React, { useRef, useState } from 'react';

interface ImageUploadProps {
  label: string;
  accept: string;
  onUpload: (file: File | null) => void;
  maxSizeMB?: number;
}

export const ImageUpload: React.FC<ImageUploadProps> = ({ label, accept, onUpload, maxSizeMB = 10 }) => {
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const handleFile = (selectedFile: File) => {
    setError(null);
    
    // Validate size
    if (selectedFile.size > maxSizeMB * 1024 * 1024) {
      setError(`File size exceeds ${maxSizeMB}MB limit.`);
      return;
    }
    
    setFile(selectedFile);
    onUpload(selectedFile);
    
    // Create preview
    const reader = new FileReader();
    reader.onload = (e) => {
      setPreview(e.target?.result as string);
    };
    reader.readAsDataURL(selectedFile);
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const removeFile = (e: React.MouseEvent) => {
    e.stopPropagation();
    setFile(null);
    setPreview(null);
    onUpload(null);
    if (inputRef.current) inputRef.current.value = '';
  };

  return (
    <div className="w-full">
      <p className="label-text mb-2">{label}</p>
      
      {!file ? (
        <div 
          onClick={() => inputRef.current?.click()}
          onDragOver={handleDragOver}
          onDrop={handleDrop}
          className="border-2 border-dashed border-navy-200 rounded-xl p-8 flex flex-col items-center justify-center cursor-pointer hover:border-primary hover:bg-navy-50 transition-colors"
        >
          <svg className="w-10 h-10 text-navy-400 mb-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
          </svg>
          <p className="text-sm font-medium text-navy-700">Click or drag and drop</p>
          <p className="text-xs text-navy-400 mt-1">PNG, JPG, BMP up to {maxSizeMB}MB</p>
        </div>
      ) : (
        <div className="relative border border-navy-200 rounded-xl overflow-hidden bg-navy-50">
          <div className="h-40 w-full flex items-center justify-center p-2">
            <img src={preview!} alt="Preview" className="max-h-full max-w-full object-contain" />
          </div>
          <div className="absolute bottom-0 inset-x-0 bg-white/90 backdrop-blur border-t border-navy-100 p-3 flex justify-between items-center">
            <div className="truncate pr-4">
              <p className="text-sm font-medium text-navy-900 truncate">{file.name}</p>
              <p className="text-xs text-navy-500">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
            </div>
            <button 
              onClick={removeFile}
              className="text-red-500 hover:text-red-700 p-1"
              title="Remove file"
            >
              <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
            </button>
          </div>
        </div>
      )}
      
      <input 
        type="file" 
        ref={inputRef} 
        className="hidden" 
        accept={accept}
        onChange={(e) => e.target.files && e.target.files[0] && handleFile(e.target.files[0])}
      />
      
      {error && <p className="text-red-500 text-xs mt-2">{error}</p>}
    </div>
  );
};
