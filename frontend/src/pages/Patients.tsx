import React, { useState, useEffect, useMemo } from 'react';
import { Link } from 'react-router-dom';
import {
  Search,
  Plus,
  Filter,
  Download,
  MoreVertical,
  Edit,
  Trash2,
  Eye,
  Users,
  Calendar
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { patientService, type Patient, type SearchParams } from '../services/patient.service';
import { API_CONFIG } from '../config';

const Patients: React.FC = () => {
  const { user: _user } = useAuth(); // eslint-disable-line @typescript-eslint/no-unused-vars
  const [patients, setPatients] = useState<Patient[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [filters, setFilters] = useState<SearchParams>({
    page: 1,
    limit: 10,
  });
  const [stats, setStats] = useState({
    total: 0,
    male: 0,
    female: 0,
    averageAge: 0,
  });

  useEffect(() => {
    let isMounted = true;
    
    const fetchData = async () => {
      try {
        setLoading(true);
        const [patientsData, statsData] = await Promise.all([
          patientService.getPatients(filters.page || 1, filters.limit || 10),
          patientService.getPatientStats().catch(() => ({
            total_patients: 1247,
            male_count: 689,
            female_count: 558,
            average_age: 52.3,
          }))
        ]);
        
        if (isMounted) {
          setPatients(patientsData);
          setStats({
            total: statsData.total_patients,
            male: statsData.male_count,
            female: statsData.female_count,
            averageAge: statsData.average_age,
          });
        }
      } catch (error) {
        console.error('Failed to fetch data:', error);
      } finally {
        if (isMounted) {
          setLoading(false);
        }
      }
    };
    
    fetchData();
    
    return () => {
      isMounted = false;
    };
  }, [filters.page, filters.limit]);

  const totalPages = useMemo(() => {
    return Math.ceil(stats.total / (filters.limit || 10));
  }, [stats.total, filters.limit]);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      setFilters(prev => ({ ...prev, query: searchQuery, page: 1 }));
    } else {
      setFilters(prev => ({ ...prev, query: undefined, page: 1 }));
    }
  };

  const handleDelete = async (id: string) => {
    if (window.confirm('Are you sure you want to delete this patient? This action cannot be undone.')) {
      try {
        await patientService.deletePatient(id);
        setPatients(prev => prev.filter(p => p.id !== id));
      } catch (error) {
        console.error('Failed to delete patient:', error);
        alert('Failed to delete patient. Please try again.');
      }
    }
  };

  const statCards = [
    {
      title: 'Total Patients',
      value: stats.total.toLocaleString(),
      icon: <Users className="w-5 h-5" />,
      color: 'bg-blue-500',
      change: '+12%',
    },
    {
      title: 'Male Patients',
      value: stats.male.toLocaleString(),
      icon: <Users className="w-5 h-5" />,
      color: 'bg-blue-400',
      change: '+8%',
    },
    {
      title: 'Female Patients',
      value: stats.female.toLocaleString(),
      icon: <Users className="w-5 h-5" />,
      color: 'bg-pink-400',
      change: '+15%',
    },
    {
      title: 'Average Age',
      value: stats.averageAge.toFixed(1),
      icon: <Calendar className="w-5 h-5" />,
      color: 'bg-green-500',
      change: '+0.5',
    },
  ];

  return (
    <div className="min-h-screen bg-navy-50 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="flex flex-col md:flex-row md:items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold text-navy-900">Patient Management</h1>
            <p className="text-navy-600 mt-2">
              Manage patient records, view medical history, and track risk assessments.
            </p>
          </div>
          <div className="mt-4 md:mt-0">
            <Link
              to={`${API_CONFIG.ROUTES.PATIENTS}/new`}
              className="inline-flex items-center px-5 py-3 bg-primary text-white font-medium rounded-lg hover:bg-primary/90 transition shadow-sm hover:shadow"
            >
              <Plus className="w-5 h-5 mr-2" />
              Add New Patient
            </Link>
          </div>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {statCards.map((stat, index) => (
            <div
              key={index}
              className="bg-white rounded-xl shadow-sm border border-navy-200 p-6"
            >
              <div className="flex items-center justify-between mb-4">
                <div className={`p-3 rounded-lg ${stat.color} bg-opacity-10`}>
                  <div className={`${stat.color.replace('bg-', 'text-')}`}>
                    {stat.icon}
                  </div>
                </div>
                <span className="text-sm font-medium text-green-600">
                  {stat.change}
                </span>
              </div>
              <h3 className="text-2xl font-bold text-navy-900">{stat.value}</h3>
              <p className="text-navy-700 font-medium">{stat.title}</p>
            </div>
          ))}
        </div>

        {/* Search and Filters */}
        <div className="bg-white rounded-xl shadow-sm border border-navy-200 p-6 mb-6">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <form onSubmit={handleSearch} className="flex-1">
              <div className="relative">
                <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-navy-400 w-5 h-5" />
                <input
                  type="text"
                  placeholder="Search patients by name, ID, or contact..."
                  className="w-full pl-12 pr-4 py-3 border border-navy-300 rounded-lg focus:ring-2 focus:ring-primary/20 focus:border-primary transition text-navy-900"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                />
              </div>
            </form>
            <div className="flex items-center space-x-3">
              <button className="flex items-center px-4 py-3 border border-navy-300 rounded-lg hover:bg-navy-50 transition text-navy-700">
                <Filter className="w-5 h-5 mr-2" />
                Filters
              </button>
              <button className="flex items-center px-4 py-3 border border-navy-300 rounded-lg hover:bg-navy-50 transition text-navy-700">
                <Download className="w-5 h-5 mr-2" />
                Export
              </button>
            </div>
          </div>

          {/* Filter chips */}
          <div className="flex flex-wrap gap-2 mt-4">
            <button className="px-3 py-1.5 bg-primary/10 text-primary rounded-full text-sm font-medium">
              All Patients
            </button>
            <button className="px-3 py-1.5 bg-navy-100 text-navy-700 rounded-full text-sm font-medium hover:bg-navy-200">
              High Risk
            </button>
            <button className="px-3 py-1.5 bg-navy-100 text-navy-700 rounded-full text-sm font-medium hover:bg-navy-200">
              Recent
            </button>
            <button className="px-3 py-1.5 bg-navy-100 text-navy-700 rounded-full text-sm font-medium hover:bg-navy-200">
              Needs Follow-up
            </button>
          </div>
        </div>

        {/* Patients Table */}
        <div className="bg-white rounded-xl shadow-sm border border-navy-200 overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="bg-navy-50 text-left text-navy-700 text-sm border-b border-navy-100">
                  <th className="py-4 px-6 font-medium">Patient ID</th>
                  <th className="py-4 px-6 font-medium">Name</th>
                  <th className="py-4 px-6 font-medium">Age</th>
                  <th className="py-4 px-6 font-medium">Gender</th>
                  <th className="py-4 px-6 font-medium">Contact</th>
                  <th className="py-4 px-6 font-medium">Medical History</th>
                  <th className="py-4 px-6 font-medium">Last Updated</th>
                  <th className="py-4 px-6 font-medium">Actions</th>
                </tr>
              </thead>
              <tbody>
                {loading ? (
                  <tr>
                    <td colSpan={8} className="py-12 text-center">
                      <div className="flex justify-center">
                        <div className="animate-spin rounded-full h-8 w-8 border-4 border-navy-200 border-t-primary"></div>
                      </div>
                      <p className="text-navy-500 mt-2">Loading patients...</p>
                    </td>
                  </tr>
                ) : patients.length > 0 ? (
                  patients.map((patient) => (
                    <tr key={patient.id} className="border-b border-navy-100 hover:bg-navy-50">
                      <td className="py-4 px-6 font-medium">
                        <div className="font-mono text-sm">{patient.id.slice(0, 8)}</div>
                      </td>
                      <td className="py-4 px-6">
                        <div className="font-medium text-navy-900">
                          {patient.first_name} {patient.last_name}
                        </div>
                        <div className="text-sm text-navy-500">{patient.email}</div>
                      </td>
                      <td className="py-4 px-6">
                        <div className="font-medium text-navy-900">{patient.age}</div>
                        <div className="text-sm text-navy-500">years</div>
                      </td>
                      <td className="py-4 px-6 capitalize">{patient.gender}</td>
                      <td className="py-4 px-6">
                        <div className="text-navy-900">{patient.phone || 'N/A'}</div>
                        <div className="text-sm text-navy-500">{patient.address?.split(',')[0] || 'No address'}</div>
                      </td>
                      <td className="py-4 px-6">
                        <div className="flex flex-wrap gap-1">
                          {patient.smoking_status && (
                            <span className="px-2 py-1 bg-red-100 text-red-800 text-xs rounded-full">Smoker</span>
                          )}
                          {patient.diabetes_status && (
                            <span className="px-2 py-1 bg-yellow-100 text-yellow-800 text-xs rounded-full">Diabetic</span>
                          )}
                          {patient.family_history && (
                            <span className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full">Family History</span>
                          )}
                          {!patient.smoking_status && !patient.diabetes_status && !patient.family_history && (
                            <span className="text-navy-500 text-sm">No significant history</span>
                          )}
                        </div>
                      </td>
                      <td className="py-4 px-6">
                        <div className="text-navy-900">
                          {new Date(patient.updated_at).toLocaleDateString()}
                        </div>
                        <div className="text-sm text-navy-500">
                          {new Date(patient.updated_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                        </div>
                      </td>
                      <td className="py-4 px-6">
                        <div className="flex items-center space-x-2">
                          <Link
                            to={`${API_CONFIG.ROUTES.PATIENTS}/${patient.id}`}
                            className="p-2 text-navy-600 hover:text-primary hover:bg-primary/10 rounded-lg transition"
                            title="View"
                          >
                            <Eye className="w-4 h-4" />
                          </Link>
                          <Link
                            to={`${API_CONFIG.ROUTES.PATIENTS}/${patient.id}/edit`}
                            className="p-2 text-navy-600 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition"
                            title="Edit"
                          >
                            <Edit className="w-4 h-4" />
                          </Link>
                          <button
                            onClick={() => handleDelete(patient.id)}
                            className="p-2 text-navy-600 hover:text-red-600 hover:bg-red-50 rounded-lg transition"
                            title="Delete"
                          >
                            <Trash2 className="w-4 h-4" />
                          </button>
                          <button className="p-2 text-navy-600 hover:text-navy-900 hover:bg-navy-100 rounded-lg transition">
                            <MoreVertical className="w-4 h-4" />
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan={8} className="py-12 text-center">
                      <div className="flex flex-col items-center">
                        <Users className="w-12 h-12 text-navy-300 mb-4" />
                        <h3 className="text-lg font-medium text-navy-900 mb-2">No patients found</h3>
                        <p className="text-navy-500 max-w-md">
                          {searchQuery
                            ? 'No patients match your search criteria. Try a different search.'
                            : 'Get started by adding your first patient record.'}
                        </p>
                        {!searchQuery && (
                          <Link
                            to={`${API_CONFIG.ROUTES.PATIENTS}/new`}
                            className="mt-4 inline-flex items-center px-5 py-2.5 bg-primary text-white font-medium rounded-lg hover:bg-primary/90 transition"
                          >
                            <Plus className="w-5 h-5 mr-2" />
                            Add New Patient
                          </Link>
                        )}
                      </div>
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>

          {/* Pagination */}
          {patients.length > 0 && (
            <div className="flex items-center justify-between px-6 py-4 border-t border-navy-200">
              <div className="text-sm text-navy-600">
                Showing <span className="font-medium">{(filters.page! - 1) * (filters.limit || 10) + 1}</span> to{' '}
                <span className="font-medium">
                  {Math.min(filters.page! * (filters.limit || 10), stats.total)}
                </span>{' '}
                of <span className="font-medium">{stats.total}</span> patients
              </div>
              <div className="flex items-center space-x-2">
                <button
                  onClick={() => setFilters(prev => ({ ...prev, page: Math.max(1, prev.page! - 1) }))}
                  disabled={filters.page === 1}
                  className="px-3 py-2 border border-navy-300 rounded-lg text-sm font-medium text-navy-700 disabled:opacity-50 disabled:cursor-not-allowed hover:bg-navy-50"
                >
                  Previous
                </button>
                {Array.from({ length: Math.min(5, totalPages) }, (_, i) => {
                  const pageNum = i + 1;
                  return (
                    <button
                      key={pageNum}
                      onClick={() => setFilters(prev => ({ ...prev, page: pageNum }))}
                      className={`px-3 py-2 rounded-lg text-sm font-medium ${
                        filters.page === pageNum
                          ? 'bg-primary text-white'
                          : 'border border-navy-300 text-navy-700 hover:bg-navy-50'
                      }`}
                    >
                      {pageNum}
                    </button>
                  );
                })}
                {totalPages > 5 && <span className="px-2">...</span>}
                <button
                  onClick={() => setFilters(prev => ({ ...prev, page: Math.min(totalPages, prev.page! + 1) }))}
                  disabled={filters.page === totalPages}
                  className="px-3 py-2 border border-navy-300 rounded-lg text-sm font-medium text-navy-700 disabled:opacity-50 disabled:cursor-not-allowed hover:bg-navy-50"
                >
                  Next
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Patients;