import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { FileText, Share2, Clock } from "lucide-react"
import Link from "next/link"
import React, { useState } from 'react';
import axios from 'axios';

export default function Dashboard() {
  const [fileName, setFileName] = useState('');
  const [loading, setLoading] = useState(false);

  const handleShareFile = async () => {
    setLoading(true);
    console.log(`Starting encryption for file: ${fileName}`);
    // Simulate encryption process
    try {
      const recipientEmail = 'recipient@example.com'; // Replace with actual recipient email
      // Call backend to share the file
      const response = await axios.post('/share-file', { file_name: fileName, recipient_email: recipientEmail });
      console.log(`File shared successfully: ${response.data.message}`);
    } catch (error) {
      console.error('Error sharing file:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">Dashboard</h1>
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        <Card>
          <CardHeader>
            <CardTitle>Recently Shared Files</CardTitle>
            <CardDescription>Files you've shared in the last 7 days</CardDescription>
          </CardHeader>
          <CardContent>
            <ul className="space-y-2">
              <li className="flex items-center">
                <FileText className="mr-2 h-4 w-4" />
                <span>Project Proposal.docx</span>
              </li>
              <li className="flex items-center">
                <FileText className="mr-2 h-4 w-4" />
                <span>Q3 Report.xlsx</span>
              </li>
            </ul>
            <Button asChild className="mt-4">
              <Link href="/files">View All Files</Link>
            </Button>
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>Quick Actions</CardTitle>
            <CardDescription>Common file sharing tasks</CardDescription>
          </CardHeader>
          <CardContent>
            <Button asChild className="w-full mb-2">
              <Link href="/share">
                <Share2 className="mr-2 h-4 w-4" />
                Share a File
              </Link>
            </Button>
            <Button variant="outline" className="w-full">
              <Clock className="mr-2 h-4 w-4" />
              View Expiring Shares
            </Button>
            <input type="text" value={fileName} onChange={(e) => setFileName(e.target.value)} placeholder="Enter file name" />
            <button onClick={handleShareFile} disabled={loading}>Share File</button>
            {loading && <p>Encrypting and sharing your file...</p>}
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
